---
title: Difference between /dev/random and /dev/urandom
author: nakji
date: 2023-12-28 17:56:00 +0800
tags: [linux, random, urandom]
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

> ** 아래 내용은 GPT4 기반으로 정리했습니다. **
    
## jvm 실행 옵션 중 `Djava.security.egd` 가 의미하는게 무엇인가

`Djava.security.egd` 옵션은 Java Virtual Machine(JVM)에서 암호화 작업을 위해 사용하는 엔트로피 소스를 지정하는 데 사용됩니다. 
EGD는 Entropy Gathering Daemon의 약자로, 시스템에서 무작위성(엔트로피)을 수집하는 메커니즘을 가리킵니다.

### 엔트로피란?
엔트로피는 무작위성의 정도를 나타내며, 암호화 작업에서 매우 중요합니다. 
충분한 엔트로피가 없으면 암호화 알고리즘이 예측 가능해져 보안이 약화될 수 있습니다.

### `Djava.security.egd` 옵션의 역할:
- 이 JVM 옵션을 사용하여 애플리케이션이 엔트로피를 수집할 소스를 지정할 수 있습니다.
- 예를 들어, Linux 시스템에서는 `/dev/random` 또는 `/dev/urandom` 파일을 사용하여 엔트로피를 수집할 수 있습니다.
- `/dev/random`은 블로킹 모드로 운영되어 엔트로피 풀이 충분할 때만 데이터를 제공하는 반면, `/dev/urandom`은 비블로킹이며 더 빠르지만 엔트로피가 낮을 수 있습니다.

### 옵션 사용 예: 
`-Djava.security.egd=file:/dev/urandom -jar your-application.jar`

이 명령은 JVM이 `/dev/urandom`을 사용하여 엔트로피를 수집하도록 지시합니다.

### 왜 중요한가?
- 보안 강화: 암호화 연산에 충분하고 예측 불가능한 엔트로피를 제공하여 보안을 강화합니다.
- 성능 향상: 특히 `/dev/urandom`을 사용할 경우, 엔트로피 수집 지연을 줄여 시스템의 성능을 향상시킬 수 있습니다.

애플리케이션의 보안 요구 사항과 성능 요구 사항에 따라 적절한 엔트로피 소스를 선택하는 것이 중요합니다.    

&nbsp;
## 보안 측면에서 `/dev/random`을 사용하면 어떻게 차이가 있는건가

`/dev/random`을 사용하는 것 자체가 보안을 약화시킨다는 것은 아닙니다. 
실제로 `/dev/random`은 `/dev/urandom`에 비해 엔트로피 풀을 더 엄격하게 관리하기 때문에, 이론적으로 더 강력한 보안을 제공할 수 있습니다. 
`/dev/random`은 엔트로피 풀이 충분할 때만 데이터를 제공하기 때문에 더 예측하기 어려운 데이터를 생성합니다.

문제는 성능과 가용성 측면에서 발생할 수 있습니다. 
`/dev/random`은 엔트로피 풀이 충분한 무작위성을 갖추고 있지 않으면 데이터 읽기를 차단(블로킹)합니다. 
이는 다음과 같은 상황에서 문제가 될 수 있습니다:

- 성능 저하:
시스템이 고도의 무작위성을 필요로 하는 암호화 작업을 많이 수행할 경우,
`/dev/random`은 필요한 무작위 데이터를 생성하기 위해 충분한 엔트로피를 수집할 때까지 작업을 중단시킬 수 있습니다.
이로 인해 애플리케이션의 반응성이 떨어지고, 성능이 저하될 수 있습니다.

- 가용성 문제:
특히 엔트로피가 빠르게 고갈되는 환경에서는 `/dev/random`이 데이터를 제공할 수 없는 상태가 길어질 수 있습니다.
이는 시스템이나 서비스의 가용성에 영향을 줄 수 있으며, 특히 고가용성이 중요한 서비스에는 심각한 문제가 될 수 있습니다.

반면, `/dev/urandom`은 비블로킹 방식으로 작동하며, 충분한 엔트로피가 없을 때에도 예측 불가능한 데이터를 제공합니다. 
최신 시스템에서는 `/dev/urandom`도 매우 안전하며, 대부분의 경우에 충분한 보안을 제공합니다. 
그러나 `/dev/random`을 사용하는 것이 권장되는 경우(예: 매우 높은 보안이 요구되는 키 생성 등)에는 성능 저하를 감수하면서 보안을 최우선으로 고려할 수 있습니다.

보안과 성능 사이의 균형을 고려하여, 애플리케이션의 요구 사항과 환경에 가장 적합한 옵션을 선택하는 것이 중요합니다.
