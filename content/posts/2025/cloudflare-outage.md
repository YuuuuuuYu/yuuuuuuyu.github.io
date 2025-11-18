---
title: Cloudflare outage
author: nakji
date: 2025-11-18 23:31:00 +0900
tags: [cloudflare, outage, worker, turnstile]
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
AWS 장애 사태가 약 한달이 되어가는데 Cloudflare에서도 장애가 발생했다.

한국 시간 기준으로 20시 48분 경부터 Cloudflare가 적용된 일부 서비스가 간헐적으로 500 에러가 발생했다. 현재도 대부분의 서비스가 먹통인데, 내 블로그도 초반에는 먹통이었지만 지금은 접속이 잘 되고있다.


## 장애 원인
포스팅 작성 시간 기준으로는 아직 명확한 원인이 나오지 않았다. Cloudflare 측은 문제가 발견되어 수정 작업을 진행 중인데, 아마도 대부분의 서비스가 안정화됐을 때 다시 보고해주지 않을까 싶다.

> Update - We are continuing to work on a fix for this issue.   
> Nov 18, 2025 - 14:22 UTC

> Identified - The issue has been identified and a fix is being implemented.        
> Nov 18, 2025 - 13:09 UTC

> Update - During our attempts to remediate, we have disabled WARP access in London.  Users in London trying to access the Internet via WARP will see a failure to connect.     
> Nov 18, 2025 - 13:04 UTC

> Investigating - Cloudflare is experiencing an internal service degradation. Some services may be intermittently impacted. We are focused on restoring service. We will update as we are able to remediate. More updates to follow shortly.        
> Nov 18, 2025 - 11:48 UTC


## 영향 받은 서비스
내가 확인한 서비스는 생성형 AI(`ChatGPT`, `Claude`, `Gemini` 등)는 전원 먹통이고, Gemini의 경우 페이지는 접근되지만 프롬프트 요청이 실패한다. 나무위키에 따르면 `X(구 트위터)`, `리그 오브 레전드`를 포함하여 게임 관련 프로그램인 `배틀아이`가 적용된 게임들도 먹통이라고 한다.


## 마무리
현재는 계속해서 복구 작업이 진행중이라서 정확한 원인은 모르겠지만 AWS와 다르게 사이버 공격일 가능성도 있을 것 같다. 왜냐하면 Cloudflare는 이전에 보안 취약점 문제가 있었고 DDoS 공격도 이미 있었기 때문이다.

복구 작업이 진행되는대로 내용도 다시 업데이트해야겠다.

## 참고자료
[CloudflareStatus](https://www.cloudflarestatus.com/incidents/8gmgl950y3h7)        
[나무위키](https://namu.wiki/w/Cloudflare#s-6.4)