---
title: 네이버 로그인 과정
author: nakji
date: 2024-12-24 17:56:00 +0800
tags: [naver, login, oauth]
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
🔔 **네이버 로그인 검증 과정**   

**네이버 로그인하기까지 어떤 과정을 거치는가?**

## **1. 세션 유지 및 위조 방지용 상태 토큰 생성**
```java
// CSRF 방지를 위한 상태 토큰 생성 코드
// 상태 토큰은 추후 검증을 위해 세션에 저장되어야 한다.    
public  String generateState() {
    SecureRandom random =  new  SecureRandom();
    return  new  BigInteger(130, random).toString(32);  
}    

// 상태 토큰으로 사용할 랜덤 문자열 생성  
String state = generateState();  

// 세션 또는 별도의 저장 공간에 상태 토큰을 저장 
request.session().attribute("state", state);  
return state;
```

>CSRF 공격을 방지하기 위해 애플리케이션과 사용자 간의 상태를 보유하는 고유한 세션 토큰을 만들어야 한다. 이 세션 토큰을 `상태 토큰(state token)` 이라 하며, 상태 토큰의 값은 사용자가 네이버 로그인을 진행하는 동안 유지되어야 하며 고유한 값이어야 한다. 생성한 상태 토큰은 세션이나 별도의 저장 공간에 저장해야 한다.

## **2. 로그인 인증 요청문 생성**
URL: 
```
https://nid.naver.com/oauth2.0/authorize?     
client_id={클라이언트 아이디}&      
response_type=code&     
redirect_uri={개발자 센터에 등록한 콜백 URL(URL 인코딩)}&       
state={상태 토큰}
```

### 네이버 로그인 및 동의 화면
![네이버 로그인](https://developers.naver.com/proxyapi/rawgit/naver/naver-openapi-guide/master/ko/login/web/images/img_naverid03.gif)

![네이버 정보 제공 동의](https://developers.naver.com/proxyapi/rawgit/naver/naver-openapi-guide/master/ko/login/web/images/img_naverid04.gif)

### 응답문 URL
`{개발자 센터에 등록한 콜백 URL}?state={상태 토큰}&code={인증 코드}`
>전달받은 `state` 파라미터의 값과 처음에 생성한 상태 토큰이 일치하는지 확인하여 만약 상태 토큰과 일치하지 않다면, 해당 세션은 유효하지 않다고 판단할 수 있다.

## **3. 상태 토큰 검증**
```java
// CSRF 방지를 위한 상태 토큰 검증 검증  
// 세션 또는 별도의 저장 공간에 저장된 상태 토큰과 콜백으로 전달받은 state 파라미터의 값이 일치해야 함    

// 콜백 응답에서 state 파라미터의 값을 가져옴  
String state = request.queryParams("state");    
  
// 세션 또는 별도의 저장 공간에서 상태 토큰을 가져옴  
String storedState = request.session().attribute("state");    
if(!state.euals(storedState)) {  
    return RESPONSE_UNAUTHORIZED;  //401 unauthorized  
} else {  
    Return RESPONSE_SUCCESS;  //200 success  
}
```

## **4. 접근 토큰 요청**
URL:
```
https://nid.naver.com/oauth2.0/token?     
client_id={클라이언트 아이디}&      
client_secret={클라이언트 시크릿}&          
grant_type=authorization_code&      
state={상태 토큰}&
code={인증 코드}
```

>상태 토큰에 대한 검증이 성공적으로 끝났다면 응답으로 전달받은 인증 코드를 이용해 최종 인증 값인 접근 토큰을 발급받는다. 인증 코드는 접근 토큰을 발급할 때 1번만 사용하며 이미 사용한 인증 코드는 더 이상 사용할 수 없다.

### 응답문 JSON
```json
{
    "access_token": "AAAAQosjWDJieBiQZc3to9YQp6HDLvrmyKC+6+iZ3gq7qrkqf50ljZC+Lgoqrg",
    "refresh_token": "c8ceMEJisO4Se7uGisHoX0f5JEii7JnipglQipkOn5Zp3tyP7dHQoP0zNKHUq2gY",
    "token_type": "bearer",
    "expires_in": "3600"
}
```
접근 토큰 요청에 성공하면 접근 토큰과 갱신 토큰이 포함된 JSON 형식의 결괏값을 반환한다. 접근 토큰은 `expires_in` 속성에 설정된 시간 동안 유효하기 때문에 유효 기간이 지난 뒤에는 갱신 토큰을 사용해 접근 토큰을 다시 발급받아야 한다.

## **5. 네이버 사용자 프로필 조회**
URL: `https://openapi.naver.com/v1/nid/me`
>접근 토큰을 성공적으로 발급받았다면 접근 토큰을 이용해 네이버 사용자의 프로필 정보를 조회할 수 있다. 사용자 프로필 정보는 사용자를 구분할 수 있는 식별값인 아이디와 별명, 메일 주소와 같은 사용자 정보를 포함하고 있다.

## **프로젝트에 적용**
상태 토큰 생성은 공통 유틸 함수에 만들고 이를 가져와서 사용하려고 한다. 검증 부분이 좀 고민이 되는데 위조된 값을 가져온 경우 적절한 예외 처리가 필요할 것 같다. 이를 위해 커스텀 예외 처리 클래스를 만드려고 하는데 여러 방법이 있겠지만 괜찮다고 생각한 저장소가 있다.

[우테코 Festgo](https://github.com/woowacourse-teams/2023-festa-go/tree/dev/backend/src/main/java/com/festago/common/exception)     
enum 클래스로 에러 코드를 관리하고 각 에러 타입에 맞는 커스텀 클래스를 불러와서 처리하고 있다. 이를 위해 필요한 개념을 정리하면서 설계를 해봐야겠다.

## **공부해야하는 부분**
- 커스텀 예외 클래스 구조
- NestedRuntimeException vs RuntimeException
- ResponseEntity 용도