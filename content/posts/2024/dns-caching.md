---
title: DNS 캐싱
author: nakji
date: 2024-11-14 20:08:00 +0900
tags: [dns, caching, network]
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

사용자가 도메인을 입력했을 때, 우선적으로 해당 도메인의 IP가 캐싱 되어있는지 확인하게 된다. 캐싱 되어있지않다면 해당 IP 주소와 관련된 지정 [TTL](https://www.cloudflare.com/ko-kr/learning/cdn/glossary/time-to-live-ttl)이 허용하는 기간 동안 응답을 캐시에 저장한다.

- DNS 쿼리를 조기에 확인하여 로딩 시간이 향상되고, 대역폭/CPU 소비가 줄어듬

**- DNS 캐시되지 않은 응답**
![](/images/2024/dns3.svg)

**- DNS 캐시된 응답**
![](/images/2024/dns4.svg)

### **1. 브라우저 캐싱**
: 최신 브라우저는 기본적으로 정해진 시간 동안 DNS 레코드를 캐시하도록 설계되어있다. 웹 브라우저와 가까울수록 캐시를 확인하고 IP 주소에 대한 요청을 처리하는 단계가 적어지기 때문이다.   
예시로 `Chrome`의 경우 아래 주소에서 DNS 캐시의 상태를 볼 수 있다.  
> chrome://net-internals/#dns


### **2. OS 수준 캐싱**
: 운영체제마다 DNS 캐싱 방식과 관리하는 방법이 다르지만 공통으로 DNS Resolver로 쿼리가 요청되기 전에 요청을 받는다. `Stub Resolver`라고 불리우며 DNS Resolver의 하위 집합이라고 보면 된다. DNS Resolver와의 차이점은 스스로 재귀를 수행하지 않고 캐시를 공동으로 공유되기 때문에 DNS Resolver에 캐시가 있다면 더 빨리 IP 주소를 확인하여 반환한다.

![](https://www.nslookup.io/img/how-does-dns-resolver-work.3f1ba36a.jpg)

> [DNS 조회 과정](/posts/2024/2024-11-12-dns/#dns-%EC%A1%B0%ED%9A%8C-%EA%B3%BC%EC%A0%95)에서 DNS Resolver 앞에 Stub Resolver가 추가됐다고 보면 된다.

### 장점
- **성능 향상** : 도메인 이름 해석 시간을 단축시켜 웹 페이지 로딩 속도를 개선
- **네트워크 부하 감소**: DNS 서버로의 반복적인 조회 요청을 줄여 네트워크 트래픽을 감소
- **가용성 증대**: DNS 서버에 일시적인 장애가 발생해도 캐시된 정보를 통해 도메인 해석이 가능

### 단점
- **정보의 최신화**: DNS 레코드가 변경되었을 때, 캐시된 정보가 만료될 때까지 새로운 정보를 반영하지 못함
- **보안 취약점**: `Cache Poisoning` 공격 등으로 악성 IP 주소가 캐시에 삽입될 수 있음
- **캐시 관리의 복잡성**: TTL 값 설정이 부적절할 경우, 캐시의 효율성과 최신성 사이에 균형을 맞추기 어려움

## **DNS 레코드**
: 도메인 이름과 관련된 정보를 저장하고 제공한다. 각 레코드는 특정한 목적과 기능을 가지며, 인터넷 상에서 도메인 이름 해석, 이메일 라우팅, 서비스 위치 지정 등 여러 가지 작업을 지원한다.

![](/images/2024/dns5.png)

- **A**     
: 웹사이트 접속 시 도메인 이름을 IP 주소로 해석하여 연결

- **AAAA**  
: IPv6 네트워크를 사용하는 환경에서 웹사이트 접속

- **CNAME**     
: 여러 도메인을 동일한 IP 주소로 관리할 때 사용

### **레코드별 캐싱 전략 예시**
#### **1. 자주 변경을 하는가?**
- **변경이 적은 레코드**  
: `NS`, `SOA` 레코드 등 변경이 드물게 발생하면 높은 TTL을 설정하여 캐시 효율성을 극대화할 수 있다.
- **변경이 잦은 레코드**  
: `A`, `AAAA` 등 IP 주소가 자주 변경될 가능성이 있으면 낮은 TTL을 설정하여 변경 사항을 빠르게 반영할 수 있도록 한다.

#### **2. 사용 목적**
- `A`, `AAAA`   
: 웹사이트 접속 속도를 최적화하기 위해 캐시 효율성을 높이는 것이 중요함

- `MX`  
: 이메일 서비스의 가용성과 신뢰성을 보장하기 위해, TTL과 우선순위를 신중하게 설정

#### **3. 적정 시간**
: 단위는 초(sec)로 표현하며 시스템 환경마다, 레코드마다 전부 다르겠지만 일반적으로 아래와 같이 추정한다고 한다.
- **300초 = 5분 = Very Short**  
: 빠른 변경을 위해 낮은 TTL에 초점을 맞춤

- **3,600초 = 1시간 = Short**  
: 위와 동일하게 빠른 변경을 위해 낮은 TTL에 초점을 맞춤

- **86,400초 = 1일 = Long**  
: 일일 캐시 활용에 더 초점을 둔 상태

- **604,800초 = 7일 = Very Long**  
: 흔하지 않지만, 자주 변경되지 않는 게시되거나 신뢰할 수 있는 정보가 포함된 사이트에 사용됨

## **DNS 보안**
: 캐싱은 여러 이점을 제공하지만 잘못된 정보나 만료된 레코드을 해결하지 못할 때 여러 위협을 받을 수 있다.

### **1. DNS cache poisoning(DNS spoofing)**
: DNS 캐시에 잘못된 정보를 입력하여 DNS 쿼리가 잘못된 응답을 반환하고, 사용자가 잘못된 사이트로 연결되도록 하는 행위. 공격자는 DNS 네임 서버를 가장하여 DNS Resolver에 요청을 보낸 후, 해당 쿼리를 처리할 때 응답을 위조하여 DNS 캐시를 감염시킬 수 있다. 이는 DNS 서버가 UDP를 사용하고 현재 DNS 정보에 대한 확인이 없기 때문이다.

- **DNS 캐시 악성 침입 프로세스**
![](https://www.cloudflare.com/img/learning/dns/dns-cache-poisoning/dns-cache-poisoning-attack.svg)

1. `example.com` 도메인에 대한 IP 요청
2. 권한 있는 네임 서버에 `example.com`에 대한 IP 요청
3. 권한 있는 네임 서버가 `example.com`의 IP가 `192.0.0.16`라는 것을 반환  
  3-1. (3이 실행될 때 공격자가) `example.com`의 IP가 `192.0.0.17`라는 것을 반환  

- **악성 침입된 DNS 캐시**
![](https://www.cloudflare.com/img/learning/dns/dns-cache-poisoning/dns-cache-poisoned.svg)

> `example.com(192.0.0.16)`을 원했지만 공격자에 의해 example.com를 접근할 때 `192.0.0.17`로 이동하게 된다.

### **2. 어떻게 막아야 할까?**
: 통신을 시작하기 위해 `handshake`를 수행해야 하는 TCP를 사용하는 대신, DNS 요청 및 응답에는 UDP가 사용된다. UDP는 연결이 열려 있거나 받는 사람이 받을 준비가 되었다는 보장이 없기 때문에 위조에 취약하다.  
하지만 DNS 악성 침입이 쉽지가 않은데 DNS Resolver가 실제로 권한 있는 네임 서버를 쿼리하기 때문에, 공격자가 권한 있는 네임 서버의 실제 응답이 도착하기 전의 몇 밀리초 만에 가짜 응답을 보내야 하기 때문이다. 그리고 다음과 같은 요소를 알고 있거나 추측해야 공격이 가능하다.
- 아직 캐시되지 않은 상태로 DNS 쿼리가 진행될 때
- DNS Resolver가 사용 중인 포트
  - 예전에는 모든 쿼리가 동일한 포트를 사용했지만, 이제는 매번 다른 무작위 포트를 사용함
- 요청 ID 번호
- 쿼리를 받는 권한 있는 네임 서버

### **3. DNSSEC(Domain Name System Security Extensions)**
- 기존의 DNS 레코드에 암호화 서명을 추가하여 A, AAAA, MX, CNAME 등과 같은 일반적인 레코드 유형과 함께 DNS 네임 서버에 저장된다. 관련된 서명을 점검함으로써 요청된 DNS 레코드가 권한 있는 네임 서버에서 왔으며 중간자 공격으로 삽입된 가짜 레코드와 달리 전송 중 경로에서 변경되지 않았음을 확인할 수 있다.  
- TLS/SSL과 흡사하게 공개 키 암호화 방식을 사용하여 데이터를 확인하고 인증한다. 하지만 아직 주류가 아니므로 DNS는 여전히 공격에 취약하다.

## 자료 출처
[Cloudflare](https://www.cloudflare.com/ko-kr/learning/dns/dns-cache-poisoning/)        
[NsLookup](https://www.nslookup.io/learning/what-is-a-dns-resolver/)        
[varonis](https://www.varonis.com/blog/dns-ttl#what-is-dns-ttl-used-for/)   
ChatGPT


---
## 추가 질문
### **Stub Resolver가 구체적으로 뭐지?**
- DNS 요청을 처리하는 클라이언트 측의 DNS Resolver
- 운영체제나 어플리케이션에서 실행되며, 주로 DNS 쿼리를 시작하고 결과를 반환
- 일반적으로 도메인을 입력했을 때 IP를 가져오는 것은 브라우저를 통한 방식으로   
  브라우저에서 실행되는게 아닌 경우 Stub Resolver를 우선으로 거치게 됨

### **DNS의 장비를 교체하면 캐시 웜업은 어떻게 되나?**
서버 환경, 관리자 기준마다 다르겠지만 `캐시 히트율`, `쿼리 응답시간`, `CPU/메모리 사용량` 등에 따라 방법이 달라진다.

- **트래픽 기반**   
신규 장비는 캐시가 비어 있으므로, 기존 DNS 서버의 쿼리 로그를 수집하여 자주 요청되는 도메인 목록을 추출한다. 이후 추출된 도메인으로 새로운 DNS 장비에 쿼리를 실행하여 캐시를 저장한다.

- **점진적 트래픽 전환**  
신규 장비에 일부 트래픽만 우선 전달하고 트래픽 비율을 단계적으로 증가시킨다. 이렇게 해서 캐시가 자연스럽게 채워지도록 유도한다.