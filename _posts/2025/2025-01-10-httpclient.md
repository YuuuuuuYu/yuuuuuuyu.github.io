---
title: java.net.http.HttpClient
author: nakji
date: 2025-01-10 16:43:00 +0900
categories: [Java, Http]
tags: [Java, Http, HttpClient]
pin: false
img_path: ''
---
🔔 **HttpClient 개요**   
🔔 **HttpClient 개선 과정**   
🔔 **다른 라이브러리 비교**   

## **What? Why?**
자바에서 HTTP 요청을 생성하고, 서버와 통신하며, 응답을 처리하기 위한 API        
Java 11에서 표준 라이브러리로 도입되었으며, 이전의 HttpURLConnection보다 사용하기 쉽고 기능이 풍부하다.
- 빌더 패턴 도입: HttpRequest.newBuilder()
- 역할 분리: HttpClient, HttpRequest, HttpResponse
- 비동기 처리 지원: HttpClient.sendAsync()

### **주요 클래스**
- HttpClient: HTTP 요청을 보내기 위한 클라이언트 객체를 생성
- HttpRequest: HTTP 요청의 세부 사항(URI, 메서드, 헤더 등)
- HttpResponse: 서버로부터 받은 HTTP 응답

### **주요 메서드**
- HttpClient.newHttpClient()    
> 기본 설정을 사용한 HttpClient 인스턴스를 생성     
        - 요청(GET), 프로토콜(HTTP/2), 리다이렉트(NEVER), SSL(Default)
```
HttpClient client = HttpClient.newHttpClient();
```

- HttpRequest.newBuilder()  
> 새로운 HttpRequest 빌더를 생성
```
HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create("https://foo.com/"))
        .timeout(Duration.ofMinutes(2))
        .header("Content-Type", "application/json")
        .POST(BodyPublishers.ofFile(Paths.get("file.json")))
        .build();
```    

- client.send(request, BodyHandlers.ofString())     
> 동기적으로 HTTP 요청을 보내고, 응답을 문자열로 받음
```
HttpResponse<String> response = client.send(request, BodyHandlers.ofString());
System.out.println(response.statusCode());
System.out.println(response.body());  
```

- client.sendAsync(request, BodyHandlers.ofString())    
> 비동기적으로 HTTP 요청을 보내고, 응답을 CompletableFuture로 받음
```
client.sendAsync(request, BodyHandlers.ofString())
        .thenApply(HttpResponse::body)
        .thenAccept(System.out::println);
```

## **기능 업데이트 요약**
- java 11: HttpClient 도입
- java 14: TLS 1.3 지원
- java 15: OAuth2 등 다양한 인증 방식을 지원하는 기능이 추가
- java 17: 커넥션 풀 관리 기능이 향상
- java 18~21: HTTP/3의 정식 지원이 추가, 보안 강화

## **다른 HTTP 라이브러리**
### **RestTemplate**
- 동기 방식
- 간단한 사용법: 간단한 REST 호출에 적합
- 제한 사항: 비동기나 반응형 프로그래밍을 지원하지 않으며, 기능이 제한적

```
import org.springframework.web.client.RestTemplate;

public class RestTemplateExample {
    public static void main(String[] args) {
        RestTemplate restTemplate = new RestTemplate();
        String response = restTemplate.getForObject("https://api.example.com/data", String.class);
        System.out.println(response);
    }
}
```

### **WebClient**
- 비동기 및 반응형 지원: 비동기 호출과 리액티브 스트림을 지원
- 유연성: 다양한 HTTP 요청과 응답 처리를 유연하게 지원
- 모던한 사용법: 현대적인 웹 애플리케이션에 적합

```
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

public class WebClientExample {
    public static void main(String[] args) {
        WebClient client = WebClient.create("https://api.example.com");

        Mono<String> response = client.get()
                .uri("/data")
                .retrieve()
                .bodyToMono(String.class);

        response.subscribe(System.out::println);
    }
}
```

### **비교**
![DifferenceHttpClient](https://github.com/YuuuuuuYu/yuuuuuuyu.github.io/blob/master/assets/img/posts/httpclient1.png?raw=true)


## **출처**
[Oracle](https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/HttpClient.html)    
[OpenJDK](https://openjdk.org/groups/net/httpclient/intro.html)     
ChatGPT