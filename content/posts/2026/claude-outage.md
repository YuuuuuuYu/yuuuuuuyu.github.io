---
title: What Happened to Claude? A Timeline of Service Disruptions
author: nakji
date: 2026-03-03 23:31:00 +0900
tags: [claude, outage, overload, auth]
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
최근 Claude가 2월 말부터 시작하여 오늘까지 잔 버그(?) 같은 에러가 계속 발생하고 있다. 무슨 문제길래 해결된 것 같아도 다시 발생하는 것일까?

시기가 미국-이란 전쟁과 맞물려 있어서 AWS 중동 리전 이슈, 군사 작전에 Claude를 사용하여 트래픽 급증했다는 말도 많이 나오고 있다.

### Uptime over the past 90 days
![outage](/images/2026/claude-outage.png)

## Claude Status 요약
사건 이력을 확인해 봤을 때, 3월 1일에는 특별한 이슈가 없던 것 같다.

따라서, 3월 1일 전후로 살펴보겠다.

### 2월
여러 장애가 있었지만 대표적으로 3가지로 요약된다.

#### Claude 앱, Claude Code
- 이슈: 앱이 안 열리거나 Claude Code가 파일을 과도하게 생성했다.
- 원인: 앱 업데이트 과정에서 발생한 코드 버그 (e.g. Windows 환경의 write 경합)
- 해결: 사용자가 앱을 업데이트

#### 인프라
- 이슈: `Usage reporting`이 멈추고 대시보드가 보이지 않는 현상
- 원인: 사용 데이터를 수집하고 보여주는 내부 서비스 장애
- 해결: 내부 데이터베이스 및 서비스 복구

#### 추론 모델
- 이슈: `Opus 4.6`, `Sonnet 4.6` 모델이 답변을 못 하고 대신 에러로 응답
- 원인: 트래픽 과부하 혹은 모델 서버 자체의 불안정
- 해결: `Anthropic` 측의 서버 핫픽스

### 3월
- 이슈: 서비스 전반적으로 오류 발생
- 원인: API, 로그인 인증 시스템의 불안정
- 해결: 핫픽스(라고 하지만 현재까지도 재발하는 중)

## 어떻게 대응해야할까?
Claude API를 직접적으로 사용하는 곳이 얼마나 많을지는 모르겠지만, 대체로 코딩 생산성에 사용하는 유저가 대부분이 아닐까 싶다.

### 개발 도구로서의 생산성
Claude가 먹통일 때, 다른 AI를 사용할 수 있으면 되지 않을까?

- 개인적으로 개발 도구로서 쓸 때는 컨텍스트를 어떻게 작성했는지가 제일 클 것 같다. 
Claude Code, Gemini CLI, Codex 등 여러 도구가 있지만 모델마다 프롬프트 스타일은 다르므로 같은 컨텍스트라도 다른 성능이 나온다.
- 그러므로 각 모델에 맞게 프롬프트를 커스텀해야할텐데 이 부분에서 서비스 규모에 따라 유지비용의 차이가 발생할 것 같다.
Pro 모델 가격만 본다면 월 2~3만 원 정도 책정된다. 
- 오히려 Cursor와 같이 특정 기업의 모델만 사용하지 않는 서비스가 좋을 수도 있다.
- 위처럼 새로운 모델을 추가로 사용할 때 투자 대비 수익/안정성이 단일 AI 사용할 때보다 과연 괜찮을까?

### Claude API
Claude API를 직접 사용해 보지 않았지만, 다른 API와 마찬가지로 에러가 발생한다면 그에 대한 예외 처리가 필요할 것이다. 
장애가 발생했을 때 대체할 API가 있는지, API Gateway가 설정되지 않았다면 구축하여 다른 API로 요청을 돌릴 수도 있다.

## 마무리
작년 이맘때쯤 연구독을 했었는데 하반기에 들어서 Claude를 사용할 때 불편한 점이 점점 보이기 시작했다.
- 응답 포맷(백틱 문자 등)이 깨짐
- 요청 당 입력 토큰 사이즈가 타 AI에 비해 적음
- 컨텍스트가 일정 크기가 넘어가면 채팅을 새로 해야 함

남은 구독 기간 동안 여러 AI를 거쳐봤는데 그나마 Gemini가 내 스타일대로 답변해줘서 Gemini CLI도 같이 사용할 겸 넘어가게 되었다.
물론 전체적인 답변 퀄리티만 보면 Claude가 좋긴 한데, 불편함과 결과 사이에서 저울질했던 것이 점점 기울여진 것 같다.


## 참고자료
[ClaudeStatus](https://status.claude.com)