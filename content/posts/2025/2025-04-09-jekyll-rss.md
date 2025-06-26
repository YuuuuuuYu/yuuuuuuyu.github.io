---
title: Jekyll RSS를 생성할 때, jekyll-feed로 적용해보기
author: nakji
date: 2025-04-09 02:38:00 +0900
tags: [jekyll, rss]
showToc: true
TocOpen: true
comments: true
disableHLJS: false
disableShare: false
hideSummary: false
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
UseHugoToc: true
---

### **Introduction**
The Atom Syndication Format is an XML language used for web feeds. A web feed (also called 'news feed' or 'RSS feed') is a data format used for providing users with frequently updated content. Content distributors syndicate a web feed, thereby allowing users to subscribe a channel to it. A typical scenario of web-feed use might involve the following: a content provider publishes a feed link on its site which end users can register with an aggregator program (also called a feed reader or a news reader) running on their own machines.

### **How it works**
The atom feed, in the 'feed.xml' file uses Liquid to build the XML. The file contains the following code.

### **Installation**
Step 1. Download the file [feed.xml](https://raw.githubusercontent.com/jhvanderschee/jekyllcodex/gh-pages/feed.xml)

Step 2. Save the file in the root of your Jekyll project

Step 3. Add the following line to your head/'head.html' include:

```html
<link rel="alternate" type="application/rss+xml" href="{{ site.url }}/feed.xml">
```

>**이 블로그도 지킬 페이지로 되어있어서 위 href 값이 내 URL로 되어있다. 따라서 아래 링크를 들어가 실제 코드를 복사하는 것을 추천한다.**

## **원본 링크**
[https://jekyllcodex.org/without-plugin/rss-feed/](https://jekyllcodex.org/without-plugin/rss-feed/)