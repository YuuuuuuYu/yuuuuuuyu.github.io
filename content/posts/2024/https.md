---
title: HTTPS
author: nakji
date: 2024-11-06 18:32:00 +0900
tags: [Http, Https]
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

## HTTPS (HTTP Secure)
: HTTP의 보안이 강화된 버전이다. 소켓 통신에서 일반 텍스트를 이용하는 대신에, SSL이나 TLS 프로토콜을 통해 세션 데이터를 암호화한다.

### 1. HTTP와의 차이점
![httpAndHttps](https://yuuuuuuyu.github.io/images/2024/https0.png)

요약하면 HTTPS는 다음과 같은 차이점이 있다.
- **보안성**: 보안 인증서를 통해 데이터 전송 시 암호화를 제공하여 보안을 강화
- **무결성**: 데이터가 전송 중에 변경되지 않았음을 보장
- **신뢰성**: 검색 엔진에서 우선순위를 우대받으며, 사용자에게 더 신뢰감을 보장

### 2. 동작 원리
![httpsProcess](https://yuuuuuuyu.github.io/images/2024/https1.png)

**1) URL 파싱 및 DNS 조회**
: 브라우저는 URL을 확인하고 DNS를 통해 도메인을 IP 주소로 변환하여 전달한다.

**2) 보안 연결 설정**
: 서버는 `TLS` handshake를 통해 인증서를 클라이언트에 전송한다.      
이 인증서에는 서버의 공개 키와 인증기관(CA)의 서명이 포함되어 있다.

**3) 서버 처리 및 응답 생성**
: 보안 연결이 설정되면 암호화된 요청을 서버로 보낸다.   
서버는 요청을 해독하여 요청된 데이터, 상태코드 등으로 구성된 HTTPS 응답을 생성한다.

**4) 응답 암호화 및 전송**
: 서버는 TLS를 이용하여 응답을 암호화하고 클라이언트의 브라우저로 다시 전송한다.    
이 암호화를 통해 전송되는 동안 데이터의 보안이 유지되고 데이터를 가로채더라도 내용을 해독할 수 없다.

**5) 클라이언트에서의 처리**
: 암호화된 응답을 수신한 브라우저는 이를 해독한다.  
여기에는 웹 페이지를 표시하도록 렌더링하는 작업이 포함된다.     
데이터가 완전히 전송되고 렌더링되면 TLS 연결은 종료된다.

### 3. 전달 내용 비교
**ex) HTTP 요청 (평문 전송)**

```
POST /login HTTP/1.1
Host: www.example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 40

username=alice&password=securepassword
```

**공격자가 볼 수 있는 내용**

```
POST /login HTTP/1.1
Host: www.example.com
...
```

**HTTPS 적용시 공격자가 보는 내용**

```
(읽을 수 없는 암호화된 데이터)
��#��l���*��E�J�...
```


## SSL (Secure Sockets Layer)
: 클라이언트와 서버 간의 안전한 링크를 통해 송수신되는 모든 데이터를 안전하게 보장하는 과거의 보안 표준 기술이다. 현재는 보안 취약점 때문에 TLS 프로토콜을 대신 사용하고 있으며 문제가 됐던 취약점은 아래와 같다.

- [POODLE 공격 (Padding Oracle On Downgraded Legacy Encryption)](https://ko.wikipedia.org/wiki/POODLE)
- [BEAST 공격 (Browser Exploit Against SSL/TLS)](https://docs.digicert.com/ko/certcentral/certificate-tools/discovery-user-guide/tls-ssl-endpoint-vulnerabilities/beast.html)
- [CRIME 공격 (Compression Ratio Info-leak Made Easy)](https://ko.wikipedia.org/wiki/CRIME)
- [Heartbleed 버그](https://ko.wikipedia.org/wiki/%ED%95%98%ED%8A%B8%EB%B8%94%EB%A6%AC%EB%93%9C)
- [로그 제이션 공격 (Logjam Attack)](https://access.redhat.com/ko/articles/1480443)
- [FREAK 공격 (Factoring RSA Export Keys)](https://ko.wikipedia.org/wiki/FREAK)

대체로 보안 허점을 노려 암호화된 데이터를 복호화해서 정보를 탈취하는 방식이다.

## TLS (Transport Layer Security)
: 위와 같은 문제로 TLS가 등장했으며, SSL의 취약점을 개선하고 표준으로 자리잡게 되었다.  
다음은 TLS의 버전별 개선사항이다.
![tlsVersion](https://yuuuuuuyu.github.io/images/2024/https2.png)

- **TLS 1.0**
    - SSL 3.0을 기반으로 개발된 초기 버전
    - SSL 보안취약점 일부 대응 가능
    - 현재 대부분의 환경에서 지원 중단
- **TLS 1.1**
    - 초기화 벡터(IV) 방식 개선으로 BEAST 공격 완화
    - 현재 대부분의 환경에서 지원 중단
- **TLS 1.2**
    - `SHA-256` 해시 함수 도입
    - 인증서 기반 `handshake` 강화
    - 현재 널리 사용되며, 기본 TLS 버전으로 채택
- **TLS 1.3**
    - `handshake` 과정을 대폭 간소화하여 지연 시간 감소
    - 암호화 알고리즘을 최신 것으로 제한하여 보안 강화
    - 대부분의 기존 취약점 제거 및 `PFS` 기본으로 지원

> TLS 1.3의 경우 최신 브라우저와 호환이 되지만 구버전의 브라우저는 일부 설정이 필요할 수 있음


## 자료 출처
[MDN](https://developer.mozilla.org/ko/docs/Glossary/HTTPS)     
[Medium](https://www.devskillbuilder.com/end-to-end-process-of-https-requests-and-responses-32a1f2c9868e)   
ChatGPT