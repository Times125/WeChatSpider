#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/20 18:02
@Description: 
"""
import time
import requests
import re
import random
import math
import hashlib
from urllib.parse import quote
from ..const import SearchType
from ..logger import download_logger
from ..bloomfilter import BloomFilterRedis
from ..utils import md5
from ..kafka import write2kafka
from ..parser import (
    is_404, parse_search_article_result,
    parse_article_content, parse_fulltext_url,
    parse_search_gzh_result, parse_history_url_list
)
from ..exceptions import SpiderBanError
from ..decorators import (
    timeout_decorator, common_decorator
)
from ..utils import (
    identify_captcha,
    get_proxies, headers as my_headers
)
from ..cookies import (
    suv_gen, CookiesCache
)
from ..db import (
    WeiChatArticleData, SpiderStatusDao,
    CacheMidTable, CacheDataDao)
from ..config import (
    identify_captcha_retries,
    identify_sleep_time,
    request_retries, max_search_page,
    gzh_crawl_mode, bloomfilter_wexin_sogou
)

f = set()


class WechatAPI(object):
    """
    搜狗微信检索API
    """

    def __init__(self, _headers=None, cookies=None):
        self.headers = _headers
        self.bloomfilter = BloomFilterRedis(key=bloomfilter_wexin_sogou)
        self.cookies = cookies
        self.cookies_cache = CookiesCache()
        if not self.headers:
            self.headers = my_headers

    def _set_cache(self, suv, snuid):
        # print('set_cache suv={} snuid={}'.format(suv, snuid))
        self.cookies_cache.set('SUV', suv)
        self.cookies_cache.set('SNUID', snuid)

    def _set_cookies(self, suv=None, snuid=None, referer=None):
        """
        :param suv:
        :param snuid:
        :param referer:
        :return:
        """
        suv = self.cookies_cache.get('SUV') if suv is None else suv
        snuid = self.cookies_cache.get('SNUID') if snuid is None else snuid
        self.cookies = {'SUV': suv, 'SNUID': snuid}
        headers = dict()
        if referer is not None:
            headers['Referer'] = referer
        return headers

    @common_decorator('')
    @timeout_decorator
    def _get(self, url, session, headers):
        """
        :param url:
        :param session:
        :param headers:
        :return:
        """
        _new_headers = dict()
        if headers:
            for k, v in headers.items():
                _new_headers[k] = v
        if self.headers:
            for k, v in self.headers.items():
                _new_headers[k] = v
        resp = session.get(url, headers=_new_headers, cookies=self.cookies)
        return resp

    def _unlock_sogou(self, url, session):
        """
        解锁搜狗平台验证码（6位带波浪干扰线的验证码）
        :param url: the url before captcha occur
        :param session: requests session object
        :return:recognize captcha result [True/False]
        """
        unlock_url = "http://weixin.sogou.com/antispider/thank.php"
        url_suffix = quote(url.split('/')[-1])
        cur_time = 0
        left_time = identify_captcha_retries
        while cur_time < left_time:
            tc = int(round(time.time() * 1000))
            image_resp = session.get('http://weixin.sogou.com/antispider/util/seccode.php?tc={}'.format(tc),
                                     headers={"Referer": 'http://weixi.sogou.com' + url_suffix}, )
            if image_resp.ok:
                try:
                    captcha = identify_captcha(image_resp.content)
                    data = {
                        'c': captcha,
                        'r': '%2F' + url_suffix,
                        'v': 5}
                    _h = {
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Referer': 'http://weixin.sogou.com/antispider/?from=%2F{}'.format(url_suffix)
                    }
                    # {"code": 0,"msg": "解封成功，正在为您跳转来源地址...", "id": "790884BFC2C4B78EC440C7ACC232798B"}
                    # {"code": 3,"msg": "验证码输入错误, 请重新输入！"}
                    resp = session.post(unlock_url, data=data, headers=_h).json()
                    print(captcha, resp)
                    if resp.get('code') == 0:
                        self._set_cache(suv_gen(), resp.get('id'))
                        # self._set_cache(session.cookies.get('SUID'), resp.get('id'))
                        return True
                    else:
                        cur_time += 1
                        time.sleep(identify_sleep_time)
                        continue
                except Exception as e:
                    download_logger.error('验证码识别错误', e)
                    cur_time += 1
                    time.sleep(identify_sleep_time)

            else:
                cur_time += 1
                time.sleep(identify_sleep_time)
        return False

    # TODO 需要重新测试编写代码
    def _unlock_wechat(self, url, session):
        """
        解锁微信的验证码（4位验证码）
        :param session: requests session for WeChat official accounts
        :param url:
        :return:
        """
        unlock_url = 'https://mp.weixin.qq.com/mp/verifycode'
        headers = {'Host': 'mp.weixin.qq.com',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Refer': url,
                   }
        cur_time = 0
        while cur_time < identify_captcha_retries:
            cert = time.time() * 1000
            url = 'https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(cert)
            image_resp = session.get(url, headers=headers)  # 首先获取腾讯验证码图片
            if image_resp.ok:
                try:
                    captcha = identify_captcha(image_resp.content, model_type='wechat', site='mp.weixin.qq.com')
                    # print(captcha)
                    data = {
                        'cert': cert,
                        'input': captcha,
                        'appmsg_token=': '',
                    }
                    ret = session.post(unlock_url, data=data).json()
                    # 验证成功，{"ret":0,"errmsg":"","cookie_count":0,"base_resp":{"ret":0,"errmsg":"","cookie_count":0,"sessionid":"svr_6c3bf0dc28b"},"sessionid":"svr_6c3bf0dc28b"}
                    # 验证码错误，{"ret":501,"errmsg":"","cookie_count":0,"base_resp":{"ret":501,"errmsg":"","cookie_count":0,"sessionid":"svr_496c013dfa3"},"sessionid":"svr_496c013dfa3"}
                    # 系统繁忙，{"ret":-6,"errmsg":"","cookie_count":0,"base_resp":{"ret":-6,"errmsg":"","cookie_count":0,"sessionid":"svr_496c013dfa3"},"sessionid":"svr_496c013dfa3"}
                    if ret['ret'] != 0:
                        if ret['ret'] != -6:
                            _id = hashlib.md5(image_resp.content).hexdigest()
                            if _id not in f:
                                f.add(_id)
                                with open('/home/lch/wrong_tencent/{}_{}.png'.format(captcha, _id), 'wb') as w:
                                    w.write(image_resp.content)
                                print('wrong:', captcha)
                        cur_time += 1
                        continue
                    else:
                        return True
                except Exception as e:
                    download_logger.error("解锁腾讯的验证码出错{}".format(e))
                    cur_time += 1
        return False

    @timeout_decorator
    def _get_with_unlock(self, url, session=None, referer=None, captcha_recognize_func=None):
        """
        获取网页并破解验证码
        :param url:
        :param session:
        :param referer:
        :param captcha_recognize_func:验证码破解函数
        :return:
        """
        download_logger.info("search page {} and referer is {}".format(url, referer))
        if not session:
            session = requests.Session()
        if not callable(captcha_recognize_func):
            captcha_recognize_func = self._unlock_sogou

        _headers = self._set_cookies(referer=referer)
        resp = self._get(url, session, headers=_headers)
        resp.encoding = 'utf-8'
        if '正在跳转' in resp.text:
            print('出现验证码')
        if 'antispider' in resp.url or '请输入验证码' in resp.text:
            download_logger.warning('需要输入验证码才能继续检索微信文章！')
            flag = captcha_recognize_func(url, session)
            if not flag:
                raise SpiderBanError("spiders had been banned")
            else:
                _headers = self._set_cookies(referer=referer)
                resp = self._get(url, session, headers=_headers)
                resp.encoding = 'utf-8'
        if is_404(resp.text):
            return '404 page'
        return resp.text

    @timeout_decorator
    def _get_article_html(self, url, session=None, referer=None):
        """
        获取微信文章的网页源码
        :param url: article's link
        :param session: article's link
        :param referer:
        :return:
        """
        download_logger.info("crawl article {} ".format(url))
        if not session:
            session = requests.Session()
        count = 0
        while count < request_retries:
            _headers = self._set_cookies(referer=referer)
            resp = self._get(url, session, _headers)
            if not resp:
                count += 1
                continue
            resp.encoding = 'utf-8'
            if is_404(resp.text):
                return '404 page'
            return resp.text
        return ''

    def _get_article_content(self, keyword, session=None, article_list=[], referer=None):
        """
        根据文章URL列表，抓取具体每篇文章的详细内容，包括正文，图片链接、视频链接等
        :param article_list:
        :param session:
        :param keyword:
        :param referer:
        :return:
        """
        for item in article_list:
            # print(item)
            if not item['article_url']:
                continue
            if self.bloomfilter.is_exists(item['article_from'] + str(item['article_time'])):  # 以公众号名和文章发布时间来衡量是否重复抓取
                continue
            html = self._get_article_html(item['article_url'], session, referer)
            if not html:
                download_logger.warning("crawl content failed, the url is {}".format(item['article_url']))
                continue
            # 当出现转发，需要点阅读全文的时候，得重新获取链接加载
            if '阅读全文' in html:
                fulltext_url = parse_fulltext_url(html)
                if not fulltext_url:
                    continue
                html = self._get_article_html(fulltext_url, session, referer)
                if not html:
                    continue
            content_dict = parse_article_content(html)
            content_dict.update(item)
            self._storage(keyword, content_dict)

    @staticmethod
    def _storage(keyword, data):
        """
        对采集结果进行持久化存储
        :param keyword:
        :param data: data dict
        :return:
        """
        wx_article = WeiChatArticleData()
        wx_article.url = data['article_url']
        wx_article.title = data['article_title']
        wx_article.source = data['article_from']
        wx_article.publish_time = data['article_time']
        wx_article.abstract = data['article_abstract']
        wx_article.content = data['content']
        wx_article.image_urls = data['image_list']
        wx_article.video = data['video']
        wx_article.raw_content = data['page_source']
        wx_article.fetch_time = int(time.time() * 1000)
        wx_article.search_word = keyword
        wx_article.md5 = md5(data['article_title'] + str(data['article_time']))
        write2kafka(wx_article.to_json())  # 往kafka中写，不写mysql了
        # 更新缓存中间表
        _cache = CacheMidTable()
        _cache.url = wx_article.url
        _cache.md5 = wx_article.md5
        _cache.proxy = 0
        CacheDataDao.save(_cache)
        # pass

    def _format_url(self, url, session, referer, text):
        """
        抽取到的url并不是可以正常访问的url，需要通过重新拼接成可访问链接
        破解此段js：
        <script>
            (function () {
                $("a").on("click contextmenu", function () {
                var b = Math.floor(100 * Math.random()) + 1,
                a = this.href.indexOf("url="),
                c = this.href.indexOf("&k=");
            -1 !== a && -1 === c && (a = this.href.substr(a + 4 + parseInt("26") + b, 1), this.href += "&k=" + b + "&h=" + a)
                })
            })();
        </script>
        得到下面这段js，最后拼接起来得到最后链接
        <script>
            var url = '';
            url += 'http://mp.w';
            url += 'eixin.qq.co';
            url += 'm/s?src=11&';
            url += 'timestamp=1';
            url += '556106774&v';
            url += 'er=1566&sig';
            url += 'nature=FAn-';
            url += 'Cd*eldGV3EK';
            url += 'vobb7s3Hvuo';
            url += 'YAbzR5aRxr9';
            url += 'yVADX-l4NKArEkaOvqTK1YbklumcIoAYJV87vyQhasjjqM3TpJ6PTnw024VXmcg4NnWZQYW*Cm54U*qLL0YbpxJJ6oI&new=1';
            url.replace("@", "");
            window.location.replace(url)
        </script>

        :param url:
        :param session:
        :param referer:
        :param text:
        :return:
        """

        def _parse_url(_url, _pads):
            b = math.floor(random.random() * 100) + 1
            a = _url.find("url=")
            c = _url.find("&k=")
            if a != -1 and c == -1:
                _sum = 0
                for i in list(_pads) + [a, b]:
                    _sum += int(i)
                a = _url[_sum]  # 选择_url中第_sum个字符作为h的值
            return '{}&k={}&h={}'.format(_url, b, a)

        if url.startswith('/link?url='):
            url = 'https://weixin.sogou.com{}'.format(url)
            pads = re.findall(r'href\.substr\(a\+(\d+)\+parseInt\("(\d+)"\)\+b,1\)', text)
            url = _parse_url(url, pads[0] if pads else [])
            resp = self._get(url, session=session, headers=self._set_cookies(referer=referer))
            base_url = re.findall(r'var url = \'(.*?)\';', resp.text)
            _url = ''
            if base_url and len(base_url) > 0:
                _url = base_url[0]
            url_part = re.findall(r'url \+= \'(.*?)\';', resp.text)
            if url_part:
                _url = _url + ''.join(url_part)
            url = _url.replace('@', '')
        return url

    def crawl(self, keyword, search_type=SearchType.article):
        """
        根据关键字抓取微信文章或者公众号
        :param keyword:
        :param search_type: SearchType
        :return:
        """
        base_url = "http://weixin.sogou.com/weixin?type={}&s_from=input&query={}&ie=utf8&page={}"
        wait2crawl_page = max_search_page
        session = requests.Session()
        cur_page = 1
        while cur_page <= wait2crawl_page:
            url = base_url.format(search_type, keyword, cur_page)
            referer = base_url.format(search_type, quote(keyword), cur_page)
            try:
                html = self._get_with_unlock(url=url, session=session, referer=referer)
                # with open('test.html', 'w+', encoding='utf8') as w:
                #     w.write(html)
                if html and html is not '404 page':
                    # 搜索文章
                    if SearchType.article == search_type:
                        article_list = parse_search_article_result(html)
                        if article_list:
                            for item in article_list:
                                item['article_url'] = self._format_url(item['article_url'], session, referer, html)
                            self._get_article_content(keyword, session, article_list, referer)
                    # 搜索与给定名称完全匹配的公众号
                    if SearchType.gzh_account == search_type and gzh_crawl_mode == 'strict':
                        gzh_list = parse_search_gzh_result(html)
                        for item in gzh_list:
                            item['gzh_url'] = self._format_url(item['gzh_url'], session, referer, html)
                            account_link = item['gzh_url']  # 公众号首页链接
                            if keyword == item['gzh_name']:  # 若检索到的公众号名称与给定keyword匹配则进行抓取，否则继续检索
                                html = self._get_with_unlock(
                                    url=account_link, session=session,
                                    referer=referer, captcha_recognize_func=self._unlock_wechat)
                                url_list = parse_history_url_list(html)
                                self._get_article_content(keyword, session, url_list)
                                return
                    # 搜索所有名称模糊匹配的公众号
                    if SearchType.gzh_account == search_type and gzh_crawl_mode == 'greed':
                        gzh_list = parse_search_gzh_result(html)
                        for item in gzh_list:
                            item['gzh_url'] = self._format_url(item['gzh_url'], session, referer, html)
                            account_link = item['gzh_url']  # 公众号首页链接
                            html = self._get_with_unlock(
                                url=account_link, session=session,
                                referer=referer, captcha_recognize_func=self._unlock_wechat)
                            url_list = parse_history_url_list(html)
                            self._get_article_content(keyword, session, url_list)
            except SpiderBanError as e:
                download_logger.error(e)
                SpiderStatusDao.save_spider_status('因cookie过期，本页数据未能爬取，错误url={}'.format(url), 0)
            finally:
                cur_page += 1
                time.sleep(5)
