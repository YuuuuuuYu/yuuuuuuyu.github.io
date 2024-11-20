---
title: TCP/IP 4계층
author: nakji
date: 2024-11-20 11:08:00 +0900
categories: [Theory, Network]
tags: [TCP/IP, OSI]
pin: false
img_path: ''
---
🔔 **TCP/IP 모델의 개념과 동작 원리**   
🔔 **TCP/IP 모델 계층별 특징**     
🔔 **TCP와 IP 비교**   

## **What? Why?**
OSI 7 Layer 모델이 이론적 모델로 만들어진 것에 비해 TCP/IP 4 layer 모델은 실제 인터넷 프로토콜을 반영하여 실용적으로 설계되었다.

![tcpipLayer](https://blog.kakaocdn.net/dn/Go5Mi/btrKwcuCMl2/KNImS8Scha5xinTYAyNm11/img.png)  

## **OSI 모델과의 차이점**
### Application
OSI 모델에서 상위 3개의 계층이 통합된 모습인데, 실제 네트워크에서는 OSI 모델의 각 계층이 반드시 구분될 필요가 없다. 기능이 중복되거나 복잡해지기 때문에 단순화가 필요했다.

### Network Access
OSI 모델에서 물리 계층이 빠진 모습인데, 물리적 전송 매체와 데이터(Frame)를 하나의 계층에서 관리함으로써 설계를 단순화하고, 다양한 물리 매체에 대한 호환성을 높였다.

## **계층별 특징**
### L4, Application
- 사용자와 네트워크 간의 인터페이스 제공
- 이메일, 파일 전송, 웹 브라우징 등 지원
- HTTP, FTP, SMTP, DNS

### L3, Transport
- 호스트 간의 데이터 전송을 관리
- 데이터를 패킷으로 분할, 전송, 재조립, 오류 검출 및 복구를 담당
- TCP, UDP

### L2, Internet
- 네트워크 간의 데이터 패킷을 전달
- IP 주소 지정, 라우팅, 패킷 포워딩을 담당
- IP, ICMP, ARP

### L1, Network Access
- 물리적 네트워크 매체를 통해 데이터 전송
- 데이터의 물리적 전송, 프레이밍(Framing), 오류 검출을 담당
- Ethernet, Wi-Fi

![tcpipLayerProcess](https://blog.kakaocdn.net/dn/cdqn09/btrKvP0Gc6d/AEP6VGC9fJf8VsaByuUIwk/img.png)


## **TCP vs IP**
`TCP/IP`의 주요 작업은 데이터를 다른 장치로 전송하는 것인데, 중요한 것은 데이터를 정확하게 전달하여 수신 측과 발신 측의 데이터가 동일하도록 하는 것이다.      
이 과정에서 `IP`는 데이터를 목적지까지 전달하는 역할을 하고, `TCP`는 그 데이터가 정확하게 전달되도록 보장한다. 이 두 프로토콜이 함께 작동하여 신뢰성 있는 통신이 가능하게 된다.

### TCP(Transmission Control Protocol)
- 데이터의 신뢰성 있는 전송 보장
- 연결 설정, 데이터 전송 확인, 손실된 패킷 재전송
- 연결형 프로토콜, 무결성 보장, 속도 느림

### IP(Internet Protocol)
- 데이터 패킷의 주소 지정과 전달
- 경로 설정, 데이터 패킷 라우팅
- 비연결형 프로토콜, 무결성 보장 못함, 속도 빠름


## **동작 원리**
![tcpipLayerProcess2](https://signal.avg.com/hs-fs/hubfs/Blog_Content/Avg/Signal/AVG%20Signal%20Images/What%20is%20TCPIP%20(Signal)/TCP-IP.png?width=1320&name=TCP-IP.png)

TCP/IP 모델은 절차에 따라 해당 데이터를 패킷으로 나눈다.    
이후 한 순서로 계층을 거친 다음 수신 측에서 데이터가 다시 조립되면서 역순으로 이동한다.    
> ❗ **그림에 있는 숫자 번호가 Layer 번호를 의미하는 것이 아님**


## 자료 출처
[Geeksforgeeks](https://www.geeksforgeeks.org/tcp-ip-model/)    
[AVG](https://www.avg.com/en/signal/what-is-tcp-ip)     
[Tistory](https://mysterlee.tistory.com/40)     
ChatGPT