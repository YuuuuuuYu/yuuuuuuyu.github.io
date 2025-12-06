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

2025년 11월 18일에 이미 장애가 한 번 났는데, 2주가 좀 지난 오늘 또 장애가 발생했다. 다행히 설정 변경 직후 곧바로 감지가 되어서 장애 발생 후, 약 25분만에 문제가 해결되었다.

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

구체적으로 보안 취약점에 대응하기 위해 기본 버퍼 크기를 128KB에서 1MB로 늘려서 점진적으로 배포하고 있었다. 그런데 내부 WAF 테스트 도구가 이 버퍼 크기 변경을 지원하지 않아서 테스트 도구를 비활성화시켰는데, 이 변경이 즉각적으로 전 세계에 전파되었다. 

일부 **FL1 Proxy** 라고 불리는 구형 프록시에서는 테스트 도구를 비활성화시키는 것이 오류를 유발하여 HTTP 500 에러를 발생시키기도 했다.

> FL1 프록시의 코드 실행에서 버그로 인해 Lua 예외가 발생
```
[lua] Failed to run module rulesets callback late_routing: 
/usr/local/nginx-fl/lua/modules/init.lua:314: attempt to index field 'execute' (a nil value)
```

### 공식 블로그 내용
> Cloudflare's Web Application Firewall (WAF) provides customers with protection against malicious payloads, allowing them to be detected and blocked. To do this, Cloudflare’s proxy buffers HTTP request body content in memory for analysis. Before today, the buffer size was set to 128KB.

> As part of our ongoing work to protect customers who use React against a critical vulnerability, CVE-2025-55182, we started rolling out an increase to our buffer size to 1MB, the default limit allowed by Next.js applications, to make sure as many customers as possible were protected.

> This first change was being rolled out using our gradual deployment system. During rollout, we noticed that our internal WAF testing tool did not support the increased buffer size. As this internal test tool was not needed at that time and had no effect on customer traffic, we made a second change to turn it off.

> Unfortunately, in our FL1 version of our proxy, under certain circumstances, the second change of turning off our WAF rule testing tool caused an error state that resulted in 500 HTTP error codes to be served from our network.

> As soon as the change propagated to our network, code execution in our FL1 proxy reached a bug in our rules module which led to the following Lua exception:


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
빠르게 감지한만큼 이전 설정으로 롤백을 했다. 변경하려고 했던 부분이 완료되지 못한 것 같은데 대신 내부 시스템을 정비한다고 한다.
- **점진적 롤아웃, 빠른 롤백 기능 강화**
- **간소화된 비상 조치 기능**   
: 추가 장애가 발생하더라도 중요 작업을 계속 수행하도록 보장
- **Fail-Open 방식의 오류 처리 도입**   
: 설정 파일이 손상되거나 허용 범위를 벗어나도 요청을 차단하기보다 가능한 한 가용성을 유지하도록 변경

> We know it is disappointing that this work has not been completed yet. It remains our first priority across the organization. In particular, the projects outlined below should help contain the impact of these kinds of changes:

> Enhanced Rollouts & Versioning: Similar to how we slowly deploy software with strict health validation, data used for rapid threat response and general configuration needs to have the same safety and blast mitigation features. This includes health validation and quick rollback capabilities among other things.

> Streamlined break glass capabilities: Ensure that critical operations can still be achieved in the face of additional types of failures. This applies to internal services as well as all standard methods of interaction with the Cloudflare control plane used by all Cloudflare customers.

> "Fail-Open" Error Handling: As part of the resilience effort, we are replacing the incorrectly applied hard-fail logic across all critical Cloudflare data-plane components. If a configuration file is corrupt or out-of-range (e.g., exceeding feature caps), the system will log the error and default to a known-good state or pass traffic without scoring, rather than dropping requests.

## 영향 받은 서비스
지난 번과 다르게 Gen AI에서는 Claude만 먹통이고, ChatGPT와 Gemini는 문제가 없는듯하다.

내가 확인한 서비스 중에서는 링크드인 밖에 없지만, 단톡이나 커뮤니티에서는 티맵, 배달의민족, 요기요, 무신사 등 문제가 있는 것 같다. 또, 대부분 FL1(구형) 프록시 환경인 곳에서 오류가 발생했다고 하지만 대형 서비스에도 영향은 미친 것 같다.      
Shopify, Zoom 등

## 마무리
역시나 이번 사태에 대해 레딧에도 글이 하나 올라왔는데 거기서 괜찮은 사이트를 알게 됐다. 11월 사태에 비해 엄청 빨리 해결됐다고 생각했는데 클라우드플레어에서도 이전 사태가 발생한지 얼마 안됐고, 우선은 서비스 안정화가 우선이다보니 롤백을 바로 결정한 것 같다.

나도 이전 팀에 있었을 때, 설정 몇개 바꾸는 것으로 서비스에 문제가 생길까봐 백업을 준비한 적이 있는데 이 분야에 있는 사람이라면 한 번쯤 겪는 상황인 것 같다.

> [레딧](https://www.reddit.com/r/CloudFlare/comments/1peq60c/cloudflare_down_again/)   
> [다운 디텍터](https://downdetector.com)

## 참고자료
[CloudflareBlog](https://blog.cloudflare.com/5-december-2025-outage/)
[CloudflareStatus](https://www.cloudflarestatus.com/incidents/lfrm31y6sw9q)     
ChatGPT