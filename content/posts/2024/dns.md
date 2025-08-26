---
title: DNS (Domain Name System)
author: nakji
date: 2024-11-12 19:56:00 +0900
tags: [dns, network]
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

## **What? Why?**
사용자에게 친숙한 도메인 이름을 컴퓨터가 네트워크에서 서로를 식별하는 데 사용하는 인터넷 프로토콜(IP) 주소로 변환하는것

초기 인터넷에서는 각 컴퓨터의 이름과 IP 주소를 `호스트 파일`이라는 단일 파일에 저장하여 관리했다. 이 방식은 소규모 네트워크에서는 효과적이었지만, 인터넷이 급격히 성장하면서 수많은 도메인과 IP 주소를 관리하는 것이 비효율적이고 불가능해졌다. 이를 해결하기 위해 DNS가 개발되었는데 **분산형 계층 구조**를 통해 도메인 이름을 효율적으로 관리하고, 사용자가 웹사이트에 쉽게 접근할 수 있도록 도와준다.

요약하면 아래와 같다.
- **확장성**: 수많은 도메인과 IP 주소를 효율적으로 관리
- **편의성**: 사람이 이해하기 쉬운 도메인 이름을 사용하여 웹사이트에 접근
- **분산 관리**: 전 세계적으로 분산된 서버를 통해 빠르고 안정적인 이름 해석을 제공

## **주요 DNS 목록**
![dnsList](https://yuuuuuuyu.github.io/images/2024/dns1.png)

## **DNS 서버 유형**
![dnsServer](https://yuuuuuuyu.github.io/images/2024/dns0.png)

사용자 검색을 IP 주소로 변환하는 과정에는 네 가지 유형의 DNS 서버가 관여한다. 

### **1. 재귀 DNS 서버 (Recursive Resolver, Local DNS)**
: 사용자의 DNS 쿼리를 처음으로 받아 처리하는 서버

- 캐시된 데이터를 이용해 빠르게 응답하거나, 캐시가 없을 경우 다른 DNS 서버에 질의
- 응답 받은 데이터를 캐시에 저장하여 향후 검색 속도 향상

> 번역된 내용에서 **재귀 확인자** 또는 **재귀적 리졸버**라고 직역해서 나오는데 같은거라고 보면 됩니다.

### **2. 루트 네임 서버**
: 재귀 DNS 서버가 캐시된 데이터가 없을 때 질의를 전달하는 최상위 서버

- 최상위 도메인(TLD) 이름 서버의 위치 정보를 제공
- ICANN이 운영하는 13개의 주요 루트 서버가 존재

### **3. 최상위 도메인(TLD) 네임 서버**
: 특정 최상위 도메인(.com, .org, .net 등)에 대한 정보를 관리

- 해당 도메인 확장자에 맞는 권한 있는 이름 서버로 질의를 전달

### **4. 권한 있는 네임 서버 (Authoritative Name Server)**
: 특정 도메인에 대한 최종 DNS 응답을 제공하는 서버

- 도메인 이름과 관련된 DNS 레코드를 저장 및 제공
- 올바른 IP 주소를 재귀 DNS 서버에 반환하거나, 정보가 없을 경우 오류 메시지 전달

## **DNS 조회 과정**
![dnsLookupCloudflare](https://yuuuuuuyu.github.io/images/2024/dns2.png)

위 그림은 `example.com`을 입력했을 때 DNS를 조회하는 단계를 나타낸 것이다.

**1. 사용자 요청**
: 사용자가 웹 브라우저에 `example.com`을 입력하면 DNS Resolver에 전달된다.

**2. DNS Resolver 요청**
: 사용자의 DNS 요청을 처리하는 중간 서버로, 수신된 쿼리를 루트 서버에 전달한다.

**3. 캐시 확인**
: 캐시를 확인 후 `example.com`의 IP 주소가 있는지 확인한다. 캐시가 있으면 사용자에게 반환하고 과정이 종료되며, 캐시가 없다면 다음 단계를 진행한다.

**4. 루트 서버 조회**
: 캐시에 IP 주소가 없으므로 Resolver는 루트 서버에 쿼리를 보내고, 루트 서버는 .com TLD 서버의 주소를 반환한다.

**5. TLD 서버 조회**
: Resolver는 전달 받은 TLD 서버 주소를 보내고, 요청된 도메인의 권한 있는 네임 서버 주소를 반환한다.

**6-7. 권한 있는 네임 서버 조회**
: Resolver는 전달 받은 권한 있는 네임 서버 주소를 보내고, 최종적으로 요청된 도메인에 대한 정확한 IP 주소를 반환한다.

**8. IP 주소 반환 및 캐싱**
: 사용자한테 전달 받은 IP 주소를 반환하고 이 IP 주소를 자체 캐시에 저장하여 향후 동일한 도메인에 대한 요청 시 빠르게 응답할 수 있도록 한다.

**9. HTTP 요청 및 응답**
: 브라우저는 해당 IP 주소로 HTTP 요청을 보낸다.

**10. 웹 페이지 반환**
: 해당 IP의 서버가 브라우저에서 렌더링할 웹 페이지를 반환한다.

### **재귀 쿼리 (Recursive Query)**
: DNS 클라이언트가 DNS 서버에 모든 필요한 조회를 수행하여 최종적인 응답을 반환하도록 요청한다. 클라이언트는 하나의 요청만 보내며, DNS 서버가 필요한 모든 조회를 수행한다.

### **반복 쿼리 (Iterative Query)**
: DNS 클라이언트가 DNS 서버에 직접적으로 답변할 수 없는 경우, 다른 DNS 서버의 주소를 반환하도록 요청한다. 클라이언트는 반환된 주소로 다시 조회를 수행한다.


> **관련 내용이 너무 많아서 레코드, 캐시, 보안 등은 다음 포스트에서 이어집니다.**

## 자료 출처
[IBM](https://www.ibm.com/kr-ko/topics/dns)     
[위키백과](https://ko.wikipedia.org/wiki/%EB%8F%84%EB%A9%94%EC%9D%B8_%EB%84%A4%EC%9E%84_%EC%8B%9C%EC%8A%A4%ED%85%9C)    
[Cloudflare](https://www.cloudflare.com/ko-kr/learning/dns/what-is-dns/)    
ChatGPT


---
## 추가 질문
### **기본 DNS는 무엇인지? 아래 process의 재귀 DNS ip인가?**
기본 DNS는 사용자가 별도로 설정하지 않았을 때 자동으로 할당되는 DNS 서버이다.   
일반적으로 인터넷 서비스 제공업체(ISP)가 고객에게 기본 DNS 서버 주소를 제공하며, 컴퓨터는 이 기본 DNS 서버를 통해 도메인 이름을 해석한다.

### **DNS의 운영주체는 왜 나누어져 있는가? 운영주체가 각각의 DNS라면 내가 `naver.com`을 가고싶을때 어떤 운영주체의 DNS로 이동하는가?**
도메인은 DNS Resolver(= 기본 DNS or ISP 등)를 거치게 된다. 여기에 `naver.com`에 대한 IP 주소가 있으면 바로 사용자한테 반환하고, 주소가 없으면 그 다음 단계를 따른다.

### **보조 DNS는 의도가 무엇인가?**
기본 DNS를 보조하는 DNS 서버이다. 기본 DNS와 트래픽을 분산하여 처리할 수도 있고, 기본 DNS에 문제가 생겼을 때 대체 서버 역할을 하기도 한다.