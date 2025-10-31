---
title: 윈도우 10에서 11로 업그레이드 이후 어느 날 부팅 자체가 멈춘 일
author: nakji
date: 2025-10-31 20:04:00 +0900
tags: [windows, raid, secureboot, uefi]
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

## 개요
취준생 시절 나는 머신러닝에 관심이 생겨서 GPU가 나름 빵빵한 스펙으로 데스크탑을 구매했다.
지금 생각하면 이해가 안 가지만 왜 SSD를 2개를 샀을까? 그냥 용량 합친 것으로 1개 구매하면 됐을 텐데.
그 당시 RAID를 알게 되고 해결된 줄 알았지만 이게 지금에서야 문제가 될지는 한 달 전까지 몰랐다.

### 사건의 시작
2025년 9월에 `TPM` 설정 후 윈 11로 업그레이드하고 나서는 큰 문제가 없었는데 ***10월이 되고 몇몇 업데이트 이후*** 부팅이 멈추기 시작했다.
이때는 마침 해당 업데이트 전에 시스템 복원 지점이 생성되어 복구하는 것으로 끝났다.

이틀 전에 비슷한 상황이 발생했는데 ***시스템 복원을 하다가 복원 지점이 사라져서*** 부득이하게 재설치하게 됐다. 
하지만 하루가 지나고 같은 현상이 발생해서 하루 날 잡고 깊이 있게 파고들게 되었다.

## Windows 11 권장 환경
시스템을 복구하는 과정에서 ChatGPT와 Gemini를 많이 사용했는데, 거기서 얻은 내용을 정리하고자 한다.

### Firmware: UEFI
- Secure Boot를 활성화하기 위한 필수 모드
- 부팅 속도 향상과 2TB 이상의 디스크 용량 지원을 위함

### 보안 설정: WHQL 활성화, Secure Boot
- 운영체제 무결성 보호를 위해 필수 적용
- 부팅 과정에서 서명된 파일만 로드하고, 악성 소프트웨어가 부팅 프로세스를 가로채는 것을 차단

### 디스크 형식: GPT
- UEFI의 요구사항이며, 부트로더를 저장하는 EFI 시스템 파티션을 관리하는데 필수 요소 

### SATA: AHCI
흔한 이슈는 아니지만 RAID 모드보다 `RAID 컨트롤러`의 드라이버가 UEFI/Secure Boot 환경과 호환되지 못해 RAID 볼륨 인식에 실패했을 가능성이 높다.

## 후기
끝나고 나니까 정말 지쳤다. 재설치만 4번 정도 한 것 같은데 이래서 아는 것이 많아야 몸이 덜 힘든 것 같다.
여담으로 학생 시절 Home 버전을 Education으로 업그레이드했었다. 이걸 기준으로 Education 버전으로 재설치했는데 정품 인증이 안 돼서 Home 버전으로 다시 USB 만드는 일도 있었다.

### 기존 Windows 10 시절 BIOS 세팅
```
- SATA 모드: RAID
- Firmware 모드: Legacy + UEFI (CSM 활성화)
- 디스크 형식: MBR (Legacy 부팅)
- 보안 설정: WHQL 비활성화
```

### Windows 11 충돌 이후 최종 설정
```
- SATA 모드: AHCI
- Firmware 모드: UEFI 전용 (CSM 비활성화)
- 디스크 형식: GPT (UEFI 부팅)
- 보안 설정: WHQL 활성화 (Secure Boot 활성화)
```

## 참고
[Quasarzone](https://quasarzone.com/bbs/qc_plan/views/38497#p10)    
ChatGPT     
Gemini