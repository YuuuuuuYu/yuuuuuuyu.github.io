---
title: Photopic) AWS Lambda를 왜 써야할까?
author: nakji
date: 2025-04-05 12:55:00 +0900
tags: [photopic, aws, lambda]
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
> **[이전 포스트](/posts/2025/photopic) 를 읽고 오시는 것을 추천드립니다.**

내가 뽀또픽을 진행하면서 맡은 업무 중 이미지 업로드가 있는데, 이 작업을 하면서 왜 Lambda를 쓰게 됐는지 기록하고자 한다. 

## **초기 설계 (시작 ~ 1차 MVP)**
인프라는 AWS 서버를 사용하니 이미지 저장을 위해 S3 스토리지를 이용하고 필요한 부분이 생기면 Lambda도 사용하자는 계획이 있었다. 예시로 추후 리사이징 기능을 추가한다면 메인 서버에서 처리하기보다 람다에 리사이징을 맡기는 것이 트래픽 분산이나 유지보수에 좋다고 판단을 했다.

하지만 규모가 작은 서비스에서 굳이 Lambda를 쓰지 않아도 충분히 주요 기능을 구현했기 때문에 Lambda는 안쓰는 것으로 결정했다. 또, 1차 MVP에서 이미지 확장자를 jpg(jpeg), png, gif만 허용하기로 결정했기 때문에 람다는 쓰지 않는 방향으로 결정했다.

## **중간 수정 (1차 MVP ~ 2차 MVP)**
오히려 S3 스토리지를 Cloudflare의 R2 스토리지로 변경해야했다. 왜냐하면 AWS Lambda에서 제공하는 무료 한도량이 우리 서비스에서 발생할 수 있는 읽기/쓰기 횟수보다 높았기 때문이다. 그리고 R2 SDK가 AWS S3 기반이기 때문에 호환성도 좋았다.

![](/images/2025/photopic-aws-lambda.png)

## **최종 설계 (2차 MVP ~ 고도화)**
아이폰은 기본 확장자가 Heic, Heif 확장자를 쓰기 때문에 아이폰 유저를 고려해서라도 확장자를 추가해야했다. 하지만 자바 라이브러리에서 Heic 확장자를 호환해주지 않기 때문에 람다를 사용하여 `heic-convert` 라이브러리를 사용하는 함수를 만들었다

- 최종 이미지 업로드 확장자: `jpg(jpeg), png, gif, webP, heic, heif`

### **워크플로우**
- **jpg(jpeg), png, gif**
: 서버에서 R2 스토리지에 업로드

- **webP, heic, heif**
: 람다로 해당 파일을 스트림으로 전송 후, jpeg로 변환하여 R2 스토리지에 업로드

## **후기**
서비스의 핵심 기능 중 하나인 이미지 업로드를 구현했는데 값진 경험이었다. 최종 서비스에 이미지 업로드를 할 때, 각 이미지는 최대 10MB, 총 9개까지만 업로드할 수 있다. 로컬에서는 금방 업로드했지만 프리티어 인스턴스에서 올릴 때는 최소 3초, 최대 1분 30초까지 걸렸다. 최소는 트래픽이 없을 때 저용량 이미지 2장, 최대는 여러 테스트 도중에 평균 4MB 9장을 올렸을 때 발생한 시간이다.

실제 운영하는 것처럼 적용한다면 충분한 메모리에, 쓰레드 풀도 적용하여 업로드를 해야할 것 같다. 나는 동기식으로 적용했지만 상황에 따라서는 Cloudflare의 Image API처럼 리사이징할 때는 비동기도 필요해보인다. 좀 더 큰 서비스에서 업로드 같은 기능을 관리할 때는 어떤식으로 적용하는걸까?