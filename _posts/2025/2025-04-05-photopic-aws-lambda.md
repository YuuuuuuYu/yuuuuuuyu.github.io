---
title: Photopic) AWS Lambda를 왜 써야할까?
author: nakji
date: 2099-04-05 21:55:00 +0900
categories: [Project, photopic]
tags: [Project, AWS, Lambda]
pin: false
img_path: ''
---

## 초기 설계
AWS 서버를 사용하니 S3 스토리지를 이용하고 필요한 부분이 생기면 Lambda도 사용하자




## 중간 수정
무료 한도량을 봤을 때 Cloudflare R2 스토리지가 전반적으로 좋고, Lambda는 안써도 될것 같다




## 최종 설계
일부 확장자(webP, Heic 등)는 자바 라이브러리 호환이 되지 않기 때문에 별도 처리가 필요
-> Lambda 사용