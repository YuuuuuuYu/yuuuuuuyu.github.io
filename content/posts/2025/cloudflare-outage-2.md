---
title: "Cloudflare is down Again: What is the root cause this december?"
author: nakji
date: 2025-12-05 18:01:00 +0900
tags: [cloudflare, outage, cdn]
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

## 개요

2025년 11월 18일에 이미 장애가 한 번 났는데, 2주가 좀 지난 오늘 또 장애가 발생했다.

![outage](/images/2025/cloudflare-outage-2.png)


## 장애 원인
이번 주 공개된 ***React Server Components*** 관련하여 ***WAF의 요청 파싱 방식을 변경*** 중이었다. 그런데 변경 이후, cloudflare 네트워크 전체적으로 다운되는 현상이 발생했다.

> Resolved  
This incident has been resolved.
A change made to how Cloudflare's Web Application Firewall parses requests caused Cloudflare's network to be unavailable for several minutes this morning. This was not an attack; the change was deployed by our team to help mitigate the industry-wide vulnerability disclosed this week in React Server Components. We will share more information as we have it today.     
> Dec 05, 2025 - 09:20 UTC

> Monitoring    
A fix has been implemented and we are monitoring the results.   
> Dec 05, 2025 - 09:12 UTC

> Investigating 
Cloudflare is investigating issues with Cloudflare Dashboard and related APIs.
Customers using the Dashboard / Cloudflare APIs are impacted as requests might fail and/or errors may be displayed.     
> Dec 05, 2025 - 08:56 UTC

### React Server Components가 뭐길래?
12월 3일 React 팀에서 인증 없이 원격 코드 실행(Remote Code Execution, RCE)이 가능한 심각한 취약점을 공개했다. 해당 취약점을 요약하면 RSC에서 사용하는 “Flight” 프로토콜의 직렬화/역직렬화 처리 로직이 안전하지 않다. 공격자가 악의적으로 조작된 HTTP 요청(payload)을 보내면, 서버에서 이 데이터를 역직렬화하는 과정에서 임의의 코드가 실행될 수 있다. 

해당 기능이 실제로 `Server Function endpoint`를 직접 구현하지 않았더라도, 단순히 RSC를 지원하는 설정만으로도 취약 상태가 될 수 있다는 것이다. 이 취약점들의 공식 식별자는 다음과 같다.
> CVE-2025-55182    
> CVE-2025-66478

#### 관련 포스트
> [데일리시큐](https://www.dailysecu.com/news/articleView.html?idxno=203107)    
> [WIZ](https://www.wiz.io/blog/critical-vulnerability-in-react-cve-2025-55182)  
> [티스토리](https://gomguk.tistory.com/306)

## 조치 과정

## 영향 받은 서비스
지난 번과 다르게 Gen AI에서는 Claude만 먹통이고, ChatGPT와 Gemini는 문제가 없는듯하다.

내가 확인한 서비스 중에서는 링크드인 밖에 없지만, 단톡이나 커뮤니티에서는 티맵, 배달의민족, 요기요, 무신사 등 문제가 있는 것 같다.

## 마무리
역시나 이번 사태에 대해 레딧에도 글이 하나 올라왔는데 거기서 괜찮은 사이트를 알게 됐다.
> [레딧](https://www.reddit.com/r/CloudFlare/comments/1peq60c/cloudflare_down_again/)   
> [다운 디텍터](https://downdetector.com)

## 참고자료
[CloudflareStatus](https://www.cloudflarestatus.com/incidents/lfrm31y6sw9q)     
ChatGPT