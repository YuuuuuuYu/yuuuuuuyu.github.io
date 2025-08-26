---
title: Windows에서 WSL 설치하다가 컴퓨터 부팅도 못 할뻔한 후기
author: nakji
date: 2025-06-26 23:30:00 +0900
tags: [Windows, wsl, claude]
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

🔔 **Windows에서 WSL 설치 시 발생할 수 있는 문제**   

# WSL 설치하다가 Windows 부팅 먹통된 썰

요즘 흔히 말하는 "**바이브 코딩**"에 관심을 가져서 이것저것 하던 와중, `Claude`에서 **Claude Code**를 발표한 것을 보았다. 커서 AI를 이용한 개발은 봤지만 **Claude Code**는 기본적으로 **CLI** 방식이어서 신선했다.

**IntelliJ**나 **VSCode**에 통합하여 사용할 수도 있기 때문에 데스크탑(Windows)에 적용해보려고 WSL을 설치했다. 그런데 문제는 이때부터 시작되었다.

## 1. WSL 설치
WSL(Windows Subsystem for Linux)는 Windows에서 Linux 환경을 사용할 수 있게 해주는 기능이다. 가상머신 없이도 Windows 안에서 리눅스 환경으로 작업할 수 있다는 정도로 알고 있었다.

[Claude Code 셋업](https://docs.anthropic.com/ko/docs/claude-code/setup) 페이지 안내대로 설치를 시작했다.
```bash
npm config set os linux
```

### 1-1. 재부팅의 함정
WSL 기능을 제대로 적용하려면 재부팅해야 한다고 해서 재시작했다. **실제 문제는 여기서 시작되었다.**

부팅하면서 로딩이 돌다가 갑자기 멈췄다!?!? 강제로 재시작해봐도 같은 현상이 반복되었고, WSL 설치 문제라고 생각하여 곧바로 모바일로 여기저기 찾아봤다.

Claude를 통해 확인해보니 추정되는 원인과 해결방법을 안내해주었다
```
가능한 원인들:
- Hyper-V 충돌: WSL2는 Hyper-V를 사용하는데, 기존 가상화 소프트웨어와 충돌 가능
- BIOS/UEFI 설정: 가상화 기능이 제대로 활성화되지 않았거나 Secure Boot 설정 문제  
- Fast Startup 기능: Windows의 빠른 시작 기능이 WSL과 충돌

해결 방법:
1. 안전 모드로 부팅하여 WSL 기능 비활성화
2. BIOS에서 가상화 기능 설정 확인
3. Fast Startup 비활성화
...
```

우선 안전모드부터 들어가려고 했는데...

## 2. 안전모드부터 막힌 절망의 순간
보통 시스템에 문제가 생기면 부팅 시 "**PC 복구**" 관련 화면으로 넘어간다. 복구 화면에서 진단을 하지만 문제 해결이 안 되면 다시 재시작 또는 안전모드 재시작을 선택하게 된다.

***이렇게 되니 이상한 악순환이 만들어졌다.***
```
안전모드 시도 → PC 복구 화면 진입 → 진단 실패 → 재시작(또는 안전모드) → 무한반복
```

## 3. 마지막 희망 - 시스템 복구
WSL 기능을 비활성화하려면 최소한 안전모드라도 들어가야 하는데 그러지 못하니 답답했다. 

`Claude`가 제안한 다른 방법으로 BIOS에서 가상화 기능(AMD라서 SVM 모드)을 비활성화해봤지만, 이것도 안전모드와 동일하게 PC 복구 화면으로만 넘어갔다.

**진짜 운이 없는 건가** 싶던 찰나에, 약 2시간 전 **Windows 업데이트**를 설치했던 것이 떠올랐다. 이를 기점으로 시스템 복구가 가능했다! WSL 설치 후 바로 업데이트할까 생각도 했었는데, 다행히 내 판단이 훌륭한 백업 환경을 만들어주었다.

## 마무리
시스템 복구 전후 차이가 **WSL 설치 여부**뿐인 환경이라 원인이 명확했다. 

대부분의 개발은 Mac을 이용하지만 단순 작업이나 일상은 데스크탑을 쓰고 있는데 ***맥북 꺼내기 귀찮고 Windows에도 세팅해두면 편할 거야***라는 안일한 생각이 이 사태를 만들었다. 앞으로 개발 관련은 무조건 Mac으로만 할 것 같다.

**WSL**이 내 데스크탑에 말썽을 부린 정확한 원인은 좀 더 봐야겠지만, **Windows 11 호환성**이나 **레지스트리 충돌** 등이 원인일 수 있다고 한다. 정말로 Windows 환경에서 WSL을 다시 설치하게 되는 날이 온다면, 그때 자세히 알아볼 것 같다.

**그때까지는 만나지 말자.**