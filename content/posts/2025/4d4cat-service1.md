---
title: 사차원 주머니 프로젝트 근황 1
author: nakji
date: 2025-08-20 04:13:00 +0900
tags: [사이드프로젝트, 사차원주머니, 리팩토링]
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

🔔 **사이드 프로젝트 근황**  
🔔 **추후 개선 방향**    

## 이전 요약
사차원 주머니 프로젝트를 처음에는 개발 공부용으로만 생각했지만, 실제 서비스를 운영하는 방식으로 방향을 전환했다. 이전에는 템플릿 엔진(**`Thymeleaf`**)으로 프론트엔드를 구성하고, **`소셜 로그인`** 과 **`일별 구글 검색 키워드 순위`** 기능을 구현했었다.

### [작업 내용](/posts/2024/4d4cat1)

## 개요
하지만 이 방식은 백엔드 개발자로서 **`API Response`** 처리에 대한 고민이 부족했고, 실제 배포를 해도 사용자에게 큰 의미가 없는 웹사이트가 되어 방향성을 잃은 상태였다.

그래서 과감하게 백엔드 개발에만 집중하고 프론트엔드는 AI에게 맡기는 방식으로 구조를 변경했다. 

구체적인 내용은 다음과 같다.

## [1차 리팩토링](https://github.com/YuuuuuuYu/4d4cat-services/pull/14)
실제 서비스를 운영하려면 핵심 기능이 필요했는데, 먼저 [**`Lorem Picsum`**](https://picsum.photos) 사이트를 벤치마킹했다. 이 사이트는 페이지를 새로고침할 때마다 새로운 이미지를 보여주며, URL 파라미터로 이미지 크기나 흑백 필터 같은 옵션을 적용할 수 있다.

여기서 영감을 받아, 저작권 없는 영상이나 음원을 랜덤으로 제공하는 서비스를 구현했다. **`Lorem Picsum`** 처럼 랜덤 이미지 서비스도 계획에 있지만, 다른 곳에서 쉽게 찾아볼 수 없는 차별화된 서비스를 먼저 만들고 싶었다.

![](/images/2025/4d4cat-service1.png)

### [백엔드](https://github.com/YuuuuuuYu/4d4cat-services?tab=readme-ov-file#%EF%B8%8F-%EA%B8%B0%EC%88%A0-%EC%8A%A4%ED%83%9D)
```toml
Language: Java 21

Framework/Library: Spring Boot, Spring AOP

CI/CD: Github Actions

Infra: Gabia Cloud

AI: Claude Code, Gemini CLI
```

### 프론트엔드
```toml
Language: TypeScript

Framework/Library: React 18, Vite

UI/Styling: Tailwind CSS, Radix UI, shadcn/ui

Infra: Replit
```

템플릿 엔진을 제거하고 API 서버를 독립된 형태로 구성했지만, 사용자에게 보여줄 프론트엔드 화면이 필요했다. 그렇다고 내가 프론트엔드까지 직접 개발하며 풀스택 개발자를 지향해야 했을까? 물론 프론트엔드까지 직접 개발할 수 있다면 더할 나위 없이 좋겠지만, 나는 AI에게 맡기기로 했다.

> AI 활용(**Replit AI**)에 대해서는 다른 포스팅에서 더 자세히 다루겠다.

## 서비스 소개
세상에는 이미 많은 서비스가 있지만, 나는 최대한 기존 서비스와 겹치지 않는 특별한 기능을 제공하고 싶었다. 그래서 **`Lorem Picsum`** 사이트와 원리는 비슷하지만, 랜덤 영상과 음원을 제공한다는 차별점을 둔 서비스를 핵심 기능으로 제공하고 있다.

### Random
영상, 음원은 [Pixabay](https://pixabay.com)에서 제공하는 소스로 저작권 없고 자유롭게 사용하도록 제공한다. 기본적으로 이미지가 더 많기 때문에 랜덤 이미지 노출도 적용할 예정이다.
![](/images/2025/4d4cat-service1-video.png)
![](/images/2025/4d4cat-service1-music.png)

### Last Message
추가로 **`Last Message`** 라는 서비스를 만들었다. 이 서비스는 사이트에 접속한 사용자가 정해진 길이 내에서 원하는 메시지를 남길 수 있는 기능이다. 어떤 내용을 남길지는 온전히 사용자의 자유에 맡겨서 비속어든 칭찬이든 상관없이, 마지막에는 어떤 메시지가 남게 될지 궁금해서 만들게 되었다.
![](/images/2025/4d4cat-service1-lastmessage.png)

### Keyword
다음으로 **`키워드 통계`** 기능을 구현 중이다. 현재는 **`Google Trends`** 데이터를 실시간으로 가져와 보여주는 방식인데 추후 실시간 순위와 일별 키워드 순위를 분리하고, 클릭 이벤트를 통해 더 다양한 정보를 제공하는 것이 목표이다.

## 마무리
- 올해 초만 해도 나는 개발 공부를 위해 프로젝트의 **`존재`** 자체에만 의미를 두었다. 하지만 시간이 지나면서 좀 더 실무에 가깝게 프로젝트를 발전시키고, 백엔드 개발자로서 제 역할을 확실히 정의해야겠다는 생각으로 바뀌었다.

- 그래서 템플릿 엔진을 사용하는 대신 프론트엔드와 백엔드를 분리하여 **백엔드 코드에 더 집중**하고, 프론트엔드는 AI에게 맡겨 내가 원하는 스타일로 구현하도록 했다. 이를 통해 **`백엔드 역량`** 과 **`AI 활용 능력`** 을 함께 기를 수 있게 되었다.

이 포스팅에는 현재 어떤 서비스를 운영 중인지, 왜 리팩토링을 하게 됐는지에 대해 작성했다. 다음 사차원 주머니 포스팅에는 구체적으로 어떤 스킬이 적용했는지를 작성하고, AI를 어떤 식으로 활용했는지에 대해서도 생각 중이다.