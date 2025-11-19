---
title: "Cloudflare outage: What went wrong?"
author: nakji
date: 2025-11-18 23:31:00 +0900
tags: [cloudflare, outage, cdn, worker, turnstile]
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
AWS 장애 사태가 약 한 달이 되어가는데 Cloudflare에서도 장애가 발생했다. 한국 시간 기준으로 20시 48분경부터 Cloudflare가 적용된 일부 서비스가 간헐적으로 500 에러가 발생했다. ~현재도 대부분의 서비스가 먹통인데,~ 내 블로그도 초반에는 먹통이었지만 지금은 접속이 잘 되고 있다. 4시 28분경에 장애가 해결됐고 관련 내용을 발표했다.


## 장애 원인
~포스팅 작성 시간 기준으로는 아직 명확한 원인이 나오지 않았다. Cloudflare 측은 문제가 발견되어 수정 작업을 진행 중인데, 아마도 대부분의 서비스가 안정화됐을 때 다시 보고해 주지 않을까 싶다.~    

![outage](https://cf-assets.www.cloudflare.com/zkvhlag99gkb/3ony9XsTIteX8DNEFJDddJ/7da2edd5abca755e9088002a0f5d1758/BLOG-3079_2.png)
내부 데이터베이스 시스템 중 하나의 권한 변경이 원인이었고, 이에 따라 해당 DB가 ClickHouse 클러스터에서 반복적인 쿼리를 통해 ***feature file***을 생성하는 과정에서 중복된 항목이 다수 출력되었다. 

최근 발생한 [AWS 장애](/posts/2025/inside-the-aws-us-east-1-outage/)처럼 외부의 공격이나 악의적인 활동으로 인한 것은 아니라고 한다. 해당 파일은 봇 관리 시스템이 사용하는 파일이며, 출력 항목이 갑작스럽게 두 배로 늘어난 뒤 네트워크를 구성하는 모든 서비스로 전파되었다. 해당 파일을 참조해서 트래픽을 라우팅하거나 봇 위협을 판단하는 소프트웨어에는 해당 파일 크기 제한이 있었고, 이 수치를 넘자 장애가 발생했다.

### 이례적인 그래프
![5xxStatusVolume](https://cf-assets.www.cloudflare.com/zkvhlag99gkb/7GdZcWhEqNjwOmLcsKOXT0/fca7e6970d422d04c81b2baafb988cbe/BLOG-3079_3.png)

그래프를 보면 11:30 시점부터 트래픽이 급증하지만 이례적으로 12:00~12:30 사이에 일시적으로 회복되었다.

왜 이런 현상이 일어났는지 보면, Cloudflare 시스템은 `ClickHouse` DB 클러스터에서 실행되는 쿼리가 5분 주기로 **feature file**을 생성한다. 권한을 변경하는 과정에서 클러스터 일부 노드만 먼저 업데이트가 됐는데, 업데이트된 노드에서만 잘못된 **feature file**이 생성됐다. 업데이트되지 않은 노드에서는 정상 파일이 생성됐기 때문에 정상적인 파일, 잘못된 파일이 5분마다 랜덤하게 네트워크 전체로 전파됐다. 그래서 그래프와 같이 트래픽이 급증했다가 감소했다가 다시 급증하는 현상이 발생했다.
> 5분마다 반복: 정상 파일 -> 잘못된 파일 -> 정상 파일 -> 잘못된 파일

하지만 시간이 지나면서 클러스터 전체 노드가 업데이트되어 지속적으로 장애가 발생하게 됐다.

### Cloudflare Blog
> The issue was not caused, directly or indirectly, by a cyber attack or malicious activity of any kind. Instead, it was triggered by a change to one of our database systems' permissions which caused the database to output multiple entries into a “feature file” used by our Bot Management system. That feature file, in turn, doubled in size. The larger-than-expected feature file was then propagated to all the machines that make up our network.

> The software running on these machines to route traffic across our network reads this feature file to keep our Bot Management system up to date with ever changing threats. The software had a limit on the size of the feature file that was below its doubled size. That caused the software to fail.

> The explanation was that the file was being generated every five minutes by a query running on a ClickHouse database cluster, which was being gradually updated to improve permissions management. Bad data was only generated if the query ran on a part of the cluster which had been updated. As a result, every five minutes there was a chance of either a good or a bad set of configuration files being generated and rapidly propagated across the network.

> This fluctuation made it unclear what was happening as the entire system would recover and then fail again as sometimes good, sometimes bad configuration files were distributed to our network. Initially, this led us to believe this might be caused by an attack. Eventually, every ClickHouse node was generating the bad configuration file and the fluctuation stabilized in the failing state.

### Cloudflare Status
>Resolved   
This incident has been resolved.    
> Nov 18, 2025 - 19:28 UTC

> Update    
Cloudflare services are currently operating normally. We are no longer observing elevated errors or latency across the network.     
> Our engineering teams continue to closely monitor the platform and perform a deeper investigation into the earlier disruption, but no configuration changes are being made at this time.      
> At this point, it is considered safe to re-enable any Cloudflare services that were temporarily disabled during the incident. We will provide a final update once our investigation is complete.    
> Nov 18, 2025 - 17:44 UTC

> Update - We are continuing to work on a fix for this issue.   
> Nov 18, 2025 - 14:22 UTC

> Identified - The issue has been identified and a fix is being implemented.        
> Nov 18, 2025 - 13:09 UTC

> Update - During our attempts to remediate, we have disabled WARP access in London.  Users in London trying to access the Internet via WARP will see a failure to connect.     
> Nov 18, 2025 - 13:04 UTC

> Investigating - Cloudflare is experiencing an internal service degradation. Some services may be intermittently impacted. We are focused on restoring service. We will update as we are able to remediate. More updates to follow shortly.        
> Nov 18, 2025 - 11:48 UTC

## 조치 과정
먼저 잘못된 파일을 만들어내는 자동 쿼리 실행을 중단하고, 네트워크 전체로 퍼지지 않도록 차단했다. 그 후, 이전에 검증된 정상적인 파일을 직접 `Distribution Queue`에 넣고 강제 재시작을 했다.

지속적인 모니터링 결과, 14:30부터 에러가 감소하며 정상화되기 시작했다.

> Errors continued until the underlying issue was identified and resolved starting at 14:30. We solved the problem by stopping the generation and propagation of the bad feature file and manually inserting a known good file into the feature file distribution queue. And then forcing a restart of our core proxy.

> The remaining long tail in the chart above is our team restarting remaining services that had entered a bad state, with 5xx error code volume returning to normal at 17:06.

### 관련 내부 서비스
- Core CDN
- Turnstile
- Worker KV
- Dashboard
- Email Security
- Access

## 영향 받은 서비스
내가 확인한 서비스는 생성형 AI(`ChatGPT`, `Claude`, `Gemini` 등)는 전원 먹통이고, Gemini의 경우 페이지는 접근되지만 프롬프트 요청이 실패한다. 나무위키에 따르면 `X(구 트위터)`, `리그 오브 레전드`를 포함하여 게임 관련 프로그램인 `배틀아이`가 적용된 게임들도 먹통이라고 한다.

오프라인에서는 맥도날드 키오스크가 먹통이 됐었다.


## 마무리
~현재는 계속해서 복구 작업이 진행 중이라서 정확한 원인은 모르겠지만 AWS와 다르게 사이버 공격일 가능성도 있을 것 같다. 왜냐하면 Cloudflare는 이전에 보안 취약점 문제가 있었고 DDoS 공격도 이미 있었기 때문이다. 복구 작업이 진행되는 대로 내용도 다시 업데이트해야겠다.~

한 달 전 AWS 장애 사태를 겪고 나서 그런지 상대적으로 빨리 조치된 느낌을 받았다. 장애 초기에는 위에 언급한 대로 장애가 줄어드는 시점이 있어서 금방 조치되는 건가 싶었는데 단순히 이례적인 상황이었다.

사건이 발생하고 여러 사이트에 접속을 해봤는데 생각보다 Cloudflare도 AWS처럼 여러 곳에 적용되어있다는 것을 알게 되었다. 웬만하면 CDN 서비스는 Cloudflare를 많이 쓰는 걸까? 대부분의 사이트를 접속하면 아래 문구가 나를 맞이했다.
> 계속하려면 challenges.cloudflare.com을 차단 해제하세요.   
> Please unblock challenges.cloudflare.com to proceed.

이번에도 외부 공격보다는 내부 이슈로 발생한 장애였다. 저번에는 클라우드였고, 이번에는 CDN인데 결국 CDN도 멀티 CDN으로 관리해야 하는 걸까? 이렇게 적용한다면 비용이나 운영 측면에서 성능과 안정성을 어떻게 유지할 수 있을까?

## 참고자료
[CloudflareBlog](https://blog.cloudflare.com/18-november-2025-outage/)      
[CloudflareStatus](https://www.cloudflarestatus.com/incidents/8gmgl950y3h7)        
[나무위키](https://namu.wiki/w/Cloudflare#s-6.4)    
ChatGPT