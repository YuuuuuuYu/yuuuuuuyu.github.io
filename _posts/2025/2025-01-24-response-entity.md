---
title: springframework.http.ResponseEntity
author: nakji
date: 2025-01-23 15:00:00 +0900
categories: [Spring, Http]
tags: [Http, ResponseEntity]
pin: false
img_path: ''
---
🔔 **ResponseEntity 개요**   
🔔 **다른 방법과 비교**   

## **What? Why?**
스프링 3 버전부터 도입되었으며, 스프링 MVC에서 HTTP 응답을 다루는 주요 클래스 중 하나이다. HTTP 응답의 전체 내용을 제어할 수 있도록 해주며, 이를 통해 다음과 같은 요소들을 설정할 수 있다.

- 상태 코드 (HTTP Status Code)  
: 200 OK, 404 Not Found, 500 Internal Server Error 등

- 헤더 (Headers)    
: 응답 헤더에 특정 값을 추가/수정

- 본문 (Body)   
: 실제로 클라이언트에게 전달될 데이터

```
@GetMapping("/example")
public ResponseEntity<String> getExample() {
    String body = "Hello, World!";
    HttpHeaders headers = new HttpHeaders();
    headers.add("Custom-Header", "CustomValue");
    return new ResponseEntity<>(body, headers, HttpStatus.OK);
}
```

### **@ResponseBody**
객체를 직렬화하여 반환하는 어노테이션으로, 이것만 사용할 경우 헤더를 유연하게 설정할 수 없다.   
`@ResopnseStatus`를 사용하여 헤더를 설정할 수 있지만, 어노테이션을 별도로 추가해야하는 단점이 있다.

```
@GetMapping("/accounts/{id}")
@ResponseStatus(HttpStatus.OK)
@ResponseBody
public Account handle() {
	// ...
}
```

### **WebFlux의 Mono, Flux**
반응형 프로그래밍을 지원하는 WebFlux를 사용하는 경우, Mono나 Flux를 반환 타입으로 사용할 수 있다. 이는 비동기 및 논블로킹 방식으로 HTTP 응답을 처리할 때 유용하다.
```
@GetMapping("/reactive")
public Mono<ResponseEntity<String>> getReactive() {
    return Mono.just(ResponseEntity.ok("Hello, Reactive World!"));
}
```

따라서, SpringMVC 환경에서는 `ResponseEntity`를 사용하는 것이 바디는 물론 헤더를 제어하는데에 더 유연하게 조작이 가능하다. 물론 Http 응답을 세밀하게 제어하는 정도가 아니면 `ResponseBody`를 사용하거나 RestController를 사용하는 것이 더 좋을 수 있다.


## 자료 출처
ChatGPT