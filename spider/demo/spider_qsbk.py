# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import thread
import time

# page =1
# url = 'http://www.qiushibaike.com/hot/page/' + str(page)
# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1)'
# headers = {'User-Agent' : user_agent}
#
# try:
#     request = urllib2.Request(url, headers = headers)
#     response = urllib2.urlopen(request)
#     # print response.read()
#     content = response.read().decode('utf-8')
#     pattern = re.compile('<div.*?author clearfix">.*?<a.*?title.*?<h2>(.*?)</h2>.*?<div.*?'+
#                          'content">.*?<span>(.*?)</span>.*?<div class="stats.*?'
#                          'class="number">(.*?)</i>',re.S)
#     result = re.findall(pattern, content)
#     for [author, content, starNum] in result:
#         print author, content, starNum
#
# except urllib2.URLError, e:
#     if hasattr(e, "code"):
#         print e.code
#     if hasattr(e, "reason"):
#         print e.reason


class Spider_QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.url = 'http://www.qiushibaike.com/hot/page/'
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1)'
        self.headers = {'User-Agent' : self.user_agent}
        self.stories = []
        self.enable = False

    def getPage(self, pageIndex):
        try:
            fullurl = self.url + str(pageIndex)
            request = urllib2.Request(fullurl, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
            return None

    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "load page failed..."
            return None

        pageStories = []
        pattern = re.compile('<div.*?author clearfix">.*?<a.*?title.*?<h2>(.*?)</h2>.*?<div.*?'+
                             'content">.*?<span>(.*?)</span>.*?<div class="stats.*?'
                             'class="number">(.*?)</i>',re.S)
        result = re.findall(pattern, pageCode)
        for [author, content, starNum] in result:
            replaceBR = re.compile('<br/>')
            content_after = re.sub(replaceBR, "\n", content)
            # print author, content, starNum
            pageStories.append([author.strip(), content_after.strip(), starNum.strip()])

        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"Page:%d\nAuthor: %s\nContent: %s\nStar: %s\n" %(page, story[0], story[1], story[2])

    def start(self):
        print u"Now reading QSBK, press return to get content, Q for exit"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)

spider = Spider_QSBK()
spider.start()







