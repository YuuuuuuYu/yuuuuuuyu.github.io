---
title: HttpClient Deepdive
author: nakji
date: 2025-01-12 17:37:00 +0900
categories: [Java, Deepdive]
tags: [Java, Http, HttpClient]
pin: false
img_path: ''
---
🔔 **BodyPublisher, BodyHandler 역할**   
🔔 **HttpClient 실습**   

## **BodyPublisher? BodyHandler?**
`BodyPublisher`와 `BodyHandlers`는 요청과 응답의 본문을 처리하는 데 있어 상호 보완적인 역할을 한다. `BodyPublisher`는 클라이언트가 서버로 전송할 데이터를 정의하고, `BodyHandlers`는 서버로부터 받은 데이터를 어떻게 처리할지를 정의한다. 이 두 구성 요소를 적절히 활용하면, HTTP 통신을 더욱 유연하고 효율적으로 구현할 수 있다.

### **BodyPublisher**
- HTTP 요청의 본문을 제공
- 데이터를 전송할 때 어떻게 제공할지 정의   
    - `BodyPublishers.ofString(String)`: 문자열 데이터
    - `BodyPublishers.ofByteArray(byte[])`: 바이트 배열 데이터
    - `BodyPublishers.ofFile(Path)`: 파일 데이터
    - `BodyPublishers.ofInputStream(Supplier<InputStream>)`: 동적으로 생성되는 입력 스트림

### **BodyHandler**
- HTTP 응답의 본문을 처리하는 방법을 정의
- 서버로부터 받은 응답 데이터를 어떻게 처리할지 정의
    - `BodyHandlers.ofString()`: 문자열 데이터
    - `BodyHandlers.ofByteArray()`: 바이트 배열 데이터
    - `BodyHandlers.ofFile(Path)`: 파일 데이터
    - `BodyHandlers.ofInputStream()`: `InputStream`으로 데이터 제공

> HttpResponse.BodyHandler 클래스는 BodyHandler를 생성하기 위한 여러 가지 편리한 정적 팩토리 메서드를 제공한다. 이들 중 다수는 응답 바이트가 완전히 수신될 때까지 메모리에 축적되며, 그 후 응답 바이트는 상위 수준의 Java 유형(ofString, ofByteArray 등)으로 변환된다. 

## **Get**
### **동기**
- `BodyHandler`는 응답 상태 코드와 헤더가 사용 가능해지면 응답 본문 바이트가 수신되기 전에 호출

```
public void get(String uri, String param) throws Exception {
    String uriWithParam = uri+"?"+param;
    HttpClient client = HttpClient.newHttpClient();
    HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(uriWithParam))
            .build();

    HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
    System.out.println("Sync status code: "+ response.statusCode());
}
```

### **비동기**
- 비동기 API는 사용 가능해지면 `HttpResponse`로 완료되는 `CompletableFuture`를 즉시 반환
- `CompletableFuture.thenApply(Function)` 메서드를 사용하여 `HttpResponse`를 본문 유형, 상태 코드 등에 매핑할 수 있다.
- `join()`: 비동기 작업이 끝날 때까지 대기

```
public void getAsync(String uri, String param) {
    String uriWithParam = uri+"?"+param;
    HttpClient client = HttpClient.newHttpClient();
    HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(uriWithParam))
            .build();

    client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
            .thenApply(HttpResponse::statusCode)
            .thenAccept(statusCode -> System.out.println("Async status code: " + statusCode))
            .join();
}
```

## **Post**
- `discard BodyHandler`는 관심이 없는 응답 본문을 수신하고 삭제하는 데 사용될 수 있다. 

```
public void post(String uri, String data) throws Exception {
    HttpClient client = HttpClient.newBuilder().build();
    HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(uri))
            .POST(HttpRequest.BodyPublishers.ofString(data))
            .build();

    HttpResponse<?> response = client.send(request, HttpResponse.BodyHandlers.discarding());
    System.out.println("Post status code: " + response.statusCode());
}
```

## **실습**
### **예제**
네이버 로그인 호출에 대한 예제이다. 개인 프로젝트에 적용 중인 설정으로 `requestUrl`과 `redirectUrl`은 이미 설정되어있는 값으로 사용했다.        
실제 결과는 페이지가 리다이렉트하면서 `text/html` 타입을 반환하기 때문에 상태코드만 출력하도록 했다. 

```
public static void main(String[] args) {
    HttpClientExample httpClientExample = new HttpClientExample();
    String requestUrl = "https://nid.naver.com/oauth2.0/authorize";
    String redirectUrl = "https://4d4cat.site/login/naver/callback";
    String clientKey = "네이버키값";

    NaverLoginRequest requestParam = new NaverLoginRequest("code", clientKey, redirectUrl, "state");
    try {
        httpClientExample.get(requestUrl, requestParam.toString());
        httpClientExample.getAsync(requestUrl, requestParam.toString());
        httpClientExample.post(requestUrl, requestParam.toString());
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

### **출력**
```
Sync status code: 200
Async status code: 200
Post status code: 200
```

## **공부해야하는 개념**
- [BodySubscriber](https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/HttpResponse.BodySubscribers.html)
- [CompletableFuture](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/concurrent/CompletableFuture.html)
- Backpressure

## **[깃허브](https://github.com/YuuuuuuYu/java-httpclient-example)**