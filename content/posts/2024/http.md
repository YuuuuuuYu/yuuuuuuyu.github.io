---
title: HTTP
author: nakji
date: 2024-11-04 14:46:00 +0900
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

## HTTP (HyperText Transfer Protocol)
: **웹상에서 데이터를 송수신하기 위한 통신 규약**으로 클라이언트와 서버 사이에 이루어지는 요청/응답 프로토콜이다. 예를 들어 클라이언트인 웹 브라우저가 `HTTP`를 통하여 서버로부터 웹 페이지(HTML) 등 정보를 요청하면, 서버는 이 요청에 응답하여 필요한 정보를 사용자에게 전달한다.

> 🔔 **HTTPS를 정리하기 전, 최소한의 HTTP 정보만 정리한 것으로 일부 개념이 생략되어있습니다.**

## HTTP 요청
: HTTP 요청을 할 때, 서로 다른 유형의 정보를 전달하는 일련의 인코딩된 데이터를 전달한다.    

---

![httpRequest](https://yuuuuuuyu.github.io/images/2024/http0.png)

### 1. HTTP 버전 유형 
HTTP 버전은 시간이 지나면서 여러 버전으로 업데이트되어 왔습니다.    
간단히 요약하면 아래와 같은데 자세한 내용은 RFC 문서를 참고하시기 바랍니다. <br>    
![httpVersion](https://yuuuuuuyu.github.io/images/2024/http1.png)

- **HTTP/1.0**
    - 초기 HTTP는 각 요청마다 새로운 TCP 연결을 생성하고 종료했습니다.
    - 따라서 다수의 요청 시 지연시간이 증가합니다.
- **HTTP/1.1 (파이프라이닝)**
    - 1.0에 비해 다수의 요청을 주고 받을 수 있게 됐지만 실질적인 성능 향상에는 제한이 있습니다.
    - 현재도 레거시 환경이나 소규모 사이트에서는 사용되고 있습니다.
- **HTTP/2 (멀티플렉싱)**
    - 하나의 TCP 연결에서 여러 개의 요청과 응답을 동시에 주고받을 수 있습니다.
    - 헤더 정보를 효율적으로 압축하여 전송 데이터 크기가 줄었습니다.
    - 대다수의 사이트와 서비스에서 표준으로 채택되고 있습니다.
- **HTTP/3 (QUIC, TLS)**
    - TCP 대신 UDP 기반의 `QUIC` 프로토콜을 사용하여 연결 속도와 전송 효율성이 향상됐습니다.
    - 이전 연결 정보를 활용하여 초기 `handshake` 없이 빠르게 연결을 설정할 수 있습니다.
    - TLS 1.3이 기본적으로 통합되어 보안성이 높습니다.

### 2. 요청 메서드
서버에게 요청하는 행동이나 작업을 나타냅니다.   
요약을 하면 아래와 같은데 여기서는 일부분만 다뤄보겠습니다.<br>  
![httpMethod](https://yuuuuuuyu.github.io/images/2024/http2.png)

- **GET**
    - 특정 리소스의 표시를 요청하고, 데이터를 받기만 합니다.
- **HEAD**
    - GET 메서드의 요청과 동일한 응답을 요구하지만, 응답 본문을 포함하지 않습니다.
- **POST**
    - 특정 리소스에 엔티티를 제출할 때 쓰입니다.
- **PUT**
    - 지정된 자원의 전체 표현을 서버에 전송하여 기존 자원을 완전히 대체합니다.
- **DELETE**
    - 특정 리소스를 삭제합니다.
- **PATCH**
    - 리소스의 부분만을 수정하는데 쓰입니다.

### 3. 요청 헤더
- **User-Agent**
    - 클라이언트 소프트웨어의 정보(브라우저, 버전 등)를 전달합니다.
- **Accept**
    - 클라이언트가 처리할 수 있는 미디어 타입을 서버에 알립니다.
    - ex) text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
- **Content-Type**
    - 요청 본문의 미디어 타입을 지정합니다.   
    - `POST` `PUT` `PATCH` 요청 시 데이터 형식을 명확히 하기 위해 사용합니다.
- **Authorization**
    - 인증 정보를 포함하여 서버에 접근 권한을 전달합니다.
    - ex) Bearer abcdef123456
- **Cookie**
    - 클라이언트에 저장된 쿠키 데이터를 서버에 전송합니다.
    - 사용자 세션 관리, 상태 유지 등에 사용
- **Connection**
    - 현재 연결의 제어 옵션을 지정합니다.
    - ex) keep-alive
- **Cache-Control**
    - 요청 및 응답의 캐싱 동작을 제어합니다.
    - ex) no-cache

### 4. 요청 본문
클라이언트가 서버로 데이터를 전송할 때, 전송되는 데이터의 형식에 따라 다양한 유형이 존재합니다.
- **application/json**
    - JSON 형식의 데이터를 전송하며, 다양한 언어에서 쉽게 파싱이 가능합니다.
        ```json
        {
            "id": 123,
            "name": "홍길동",
            "email": "hong@example.com",
            "age": 30
        }
        ```
- **application/x-www-form-urlencoded**
    - HTML 폼 데이터를 키-값 형태로 인코딩하여 전송합니다.
    - 크기가 제한되어 대용량 데이터 전송에는 적합하지 않습니다.     
    `name=홍길동&email=hong%40example.com&age=30`

- **application/xml**
    - XML 형식의 데이터를 전송합니다.
    ```xml
    <user>
        <id>123</id>
        <name>홍길동</name>
        <email>hong@example.com</email>
        <age>30</age>
    </user>
    ```

## HTTP 응답

---

![HTTP 응답](https://yuuuuuuyu.github.io/images/2024/http3.png)

### 1. 응답 코드
클라이언트가 서버에 요청을 보냈을 때, 서버는 응답코드와 함께 응답합니다.
- **`1xx` (정보)**: 요청을 받았으며 프로세스를 계속한다.
- **`2xx` (성공)**: 요청을 성공적으로 받았으며 인식했고 수용하였다.
- **`3xx` (리다이렉션)**: 요청 완료를 위해 추가 작업 조치가 필요하다.
- **`4xx` (클라이언트 오류)**: 요청의 문법이 잘못되었거나 요청을 처리할 수 없다.
- **`5xx` (서버오류)**: 서버가 명백히 유효한 요청에 대해 충족을 실패했다.

### 2. 응답 헤더
- **Cache-Control**
    - 응답의 캐싱 동작을 제어합니다.
    - ex) no-cache, no-store, must-revalidate
- **Expires**
    - 클라이언트가 응답을 캐시할 수 있는 유효 기간을 설정합니다.
    - ex) Wed, 21 Oct 2025 07:28:00 GMT
- **Location**
    - 클라이언트를 다른 URL로 리디렉션합니다. 
    - 주로 3xx 리디렉션 상태 코드와 함께 사용됩니다.
- **ETag**
    - 클라이언트가 리소스의 변경 여부를 확인하는 데 사용되며, 조건부 요청에 활용됩니다.
    - 예를 들어, `If-None-Match` 헤더와 함께 사용하여 리소스의 변경 여부를 확인할 수 있습니다.
- **Access-Control-Allow-Origin**
    - CORS 정책에서 어떤 출처(origin)가 리소스에 접근할 수 있는지 지정합니다.
    - ex) Access-Control-Allow-Origin: *
- **Strict-Transport-Security (HSTS)**
    - 브라우저에게 항상 HTTPS를 사용하도록 지시합니다.
    - ex) max-age=31536000; includeSubDomains
- **Content-Security-Policy (CSP)**
    - 웹 페이지가 로드할 수 있는 리소스의 출처를 제한합니다.
    - ex) default-src 'self'; script-src 'self' https://apis.example.com

### 3. 응답 본문
- **HTML**
    - 웹 브라우저는 HTML을 해석하여 웹 페이지를 렌더링합니다.
    ```html
    <!DOCTYPE html>
    <html>
    <head>
        <title>예제 페이지</title>
    </head>
    <body>
        <h1>안녕하세요!</h1>
        <p>이것은 예제 HTML 페이지입니다.</p>
    </body>
    </html>
    ```

- **JSON**
    - RESTful API의 응답으로, 클라이언트는 이 데이터로 사용자 정보를 표시하거나 처리할 수 있습니다.
    ```json
    {
        "id": 123,
        "name": "홍길동",
        "email": "hong@example.com",
        "age": 30
    }
    ```

- **XML**
    - XML 형식으로 사용자 정보를 제공하며, 일부 레거시 시스템에서 데이터 교환에 사용됩니다.
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <user>
        <id>123</id>
        <name>홍길동</name>
        <email>hong@example.com</email>
        <age>30</age>
    </user>
    ```

## 자료 출처
[위키백과](https://ko.wikipedia.org/wiki/HTTP)  
[제타위키](https://zetawiki.com/wiki/HTTP)  
[MDN](https://developer.mozilla.org/ko/docs/Web/HTTP)   
[Cloudflare](https://www.cloudflare.com/ko-kr/learning/ddos/glossary/hypertext-transfer-protocol-http/)     
ChatGPT