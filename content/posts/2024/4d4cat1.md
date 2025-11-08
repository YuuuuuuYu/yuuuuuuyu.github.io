---
title: 4D4cat) 프로젝트 개선
author: nakji
date: 2024-12-12 15:45:00 +0900
tags: [project, 4d4cat]
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
🔔 **프로젝트 소개**   
🔔 **프로젝트 개선 과정**   


## **프로젝트 소개**
### **4d4cat 의미**
4d4cat 프로젝트는 내가 구현해보고 싶은 기능을 다 넣어서 원하는 때에 사용해보고자 만든  프로젝트이다. 이는 만화 도라에몽에서 나오는 4차원 주머니에서 여러 가지 물건을 꺼내는 것처럼 **4차원(4th-Dimension), 주머니(pocket)**를 변형해서 만든 명칭이다.

### **목적**
구현하고 싶은 기능은 크게 **데이터 수집**과 **서드 파티** 사용이다.

**데이터 수집**
- 현재 구글 트렌드 데이터 기반으로 일별 인기 검색어를 저장
- 노출 기간은 최근 한달 이내의 데이터
- 구글 트렌드 API 관련 [오픈소스](https://github.com/pat310/google-trends-api) 사용
- 인스타그램의 키워드도 수집하려고 했으나 최근에 지원 종료(예정)     

**서드 파티**
- 현재 구글 검색, 네이버 검색, ChatGPT 적용
- 아직 운영 서버에는 배포를 하지 않은 상태
- API의 일일 최대 호출 횟수가 정해져 있어서 추가 보안 설정 후에 배포 예정
- **구글 검색 화면**
![](/images/2024/4d4cat1.png)


## **프로젝트 개선하는 여정**
### **1. 여러 사용자가 각자의 패키지에서 서비스 개발**
- 한 프로젝트에 여러 사용자가 각자 서비스를 만드는게 초기 목적
- 불필요한 프로젝트 패키지 다수
- 백은 API 호출만 처리하고 프론트에서 페이지 렌더링
- 부트스트랩을 활용한 버튼 활성화 및 이미지 처리 다수

### **2. 프론트와 백을 분리하고 각각 운영해볼까?**
- 구글 트렌드 키워드만 적용한 상태로 프론트, 백 서버를 분리하여 운영
- 분리하여 운영함으로써 각각 뷰, API 호출이라는 목적을 명확히 하기 위함
- 프론트(Typescript, Node.js) / 백(Java/Spring)
- 프론트는 데이터베이스 데이터만 노출시킴
- 백은 REST API만 적용하여 필요한 데이터만 전달     
**[프론트 Github](https://github.com/YuuuuuuYu/4D4cat-Front)**

### **3. 하지만 굳이 나눠야할까? 그냥 하나로 처리하자**
- 뷰는 템플릿 엔진으로 대체하고 백엔드에서 유연하게 대체
- 초기 프로젝트 구조에서 중복 소스 제거 및 디자인 단순화
- Cloudflare를 통해 https 적용

**[리팩토링 커밋](https://github.com/YuuuuuuYu/4D4cat/commit/af8af93b874bec8e378d264deb7e7695279396e8)**


## **현재 프로젝트는?**
**[Github Pinned 참고](https://github.com/yuuuuuuyu)**