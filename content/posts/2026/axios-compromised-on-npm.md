---
title: Axios compromised on npm
author: nakji
date: 2026-04-11 16:18:00 +0900
tags: [axios, rat]
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
2026년 3월 30일(현지 시간), 주당 1억 회 이상의 다운로드를 기록하는 가장 인기 있는 HTTP 클라이언트 라이브러리인 Axios의 NPM 계정이 해킹되었다.
요약하면, Axios 관리자 계정을 탈취하고 `plain-crypto-js`라는 가짜 의존성이 추가된 ```axios@1.14.1``` 및 ```axios@0.30.4``` 버전을 배포했다.

자세한 건 아래 사이트에 정리되어 있기 때문에 나는 개발자로서 어떻게 대응해야 할지를 중점적으로 작성하려고 한다.

### 타임라인
[StepSecurity](https://www.stepsecurity.io/blog/axios-compromised-on-npm-malicious-versions-drop-remote-access-trojan)      
[SK쉴더스](https://www.skshieldus.com/security-insights/trends/axios-supply-chain-attack-insight-report)

## 대응 전략
### 1. npm install 시 `--ignore-scripts` 옵션을 사용
이번 사태에 핵심 원인이기도 했던 자동 스크립트 실행을 막는 옵션이다. 프로젝트에 따라 사용할 때도 있겠지만, 무지성 업그레이드하는 것도 지양해야 한다.

### 2. Egress 설정
아웃바운드 설정만 해도 밖으로 통신하는 것을 막기 때문에, 허용된 도메인 외에 통신은 막아두자.

### 3. Lock 파일 활용
npm, yarn 등을 사용한다면 lock 파일이 있을 텐데, 검증된 버전인지 확인하자.

### 4. 그 외
환경변수 파일을 공개적으로 올리지 않고 별도로 관리하거나, 암호화하는 것은 잘 알 것이다.

AI가 추천해 준 방법으로 패키지 내 소스 변화를 분석해 주는 `Socket.dev`, 알려진 취약점이 있는 패키지인지 확인하는 npm audit / Snyk 등도 있다.

## 마무리
Axios는 Javascript를 통해 통신을 구현해 봤다면 한 번쯤 사용해 보거나, 어떤 스킬인지는 알 것이다. 이러한 라이브러리도 보안 문제가 발생할 수 있다는 것을 알게된 사례였던 것 같다.

어찌보면 레거시 쓰는 기업들이 업그레이드를 고민하는 이유가 될 수도 있고, 무조건 최신 기술이 좋다는 것에 대한 위협을 알려준 사건이 아닌가 싶다.

## 참고자료
[Axios Github Issue](https://github.com/axios/axios/issues/10604)