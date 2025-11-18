---
title: 2025 AWS US-East-1 outage, DynamoDB down
author: nakji
date: 2025-10-21 06:20:00 +0900
tags: [aws, region, outage, dynamodb, dns, ec2, nlb]
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
> ***Thomas Eccel(구글 Ads 스페셜리스트)의 글을 포함한 외국 저널과 AWS에 Service health 내용을 참고하여 작성했습니다.***

한국 시간 기준, 2025년 10월 20일 오후 4시 경부터 `US-EAST-1` 리전을 사용하는 다수의 서비스에서 장애가 발생

**원인**: *US-EAST-1 리전의 DynamoDB API 엔드포인트의 DNS*

**영향**: IAM, DynamoDB 테이블을 포함한 US-EAST-1 엔드포인트에 의존하는 다른 서비스 

## 장애 원인
해당 리전의 DynamoDB API 엔드포인트의 DNS에서 문제가 발생했다고 하는데 구체적으로 어떤 내용일까?

> Oct 20 2:01 AM PDT We have identified a potential root cause for error rates for the DynamoDB APIs in the US-EAST-1 Region. Based on our investigation, the issue appears to be related to DNS resolution of the DynamoDB API endpoint in US-EAST-1. We are working on multiple parallel paths to accelerate recovery.

> Oct 20 8:43 AM PDT We have narrowed down the source of the network connectivity issues that impacted AWS Services. The root cause is an underlying internal subsystem responsible for monitoring the health of our network load balancers. We are throttling requests for new EC2 instance launches to aid recovery and actively working on mitigations.

> Oct 20 10:03 AM PDT We continue to apply mitigation steps for network load balancer health and recovering connectivity for most AWS services. Lambda is experiencing function invocation errors because an internal subsystem was impacted by the network load balancer health checks.

`AWS Health`에 적힌 내용을 보니 DNS 문제 때문에 IP 변환에 실패했고, 이것이 연쇄적으로 작용하여 과한 트래픽이 발생했다.

왜 실패한지에 대해서는 **모니터링/로드밸런서 서브시스템의 문제**인데, 헬스 체크나 비정상적인 상태 감지 등의 문제로 오류가 더 확대된 것이 아닐까? 

`2:01 AM PDT` 내용을 보면 복구하기 위해 복합적으로 연구 중인 것으로 보이는데 단순 재기동이 아니라 DNS 경로를 다시 설정하고, 로드밸런서를 복구하고, 백로그 처리 등 필요해보인다.

이로 인해 다른 서비스(EC2, IAM, 특히 Lambda)까지 영향을 준 것으로 보인다.

### Reddit에 올라온 하나의 글
**How TF did AWS mess up so bad that the entire us-east-1 region is down, all 6 AZs are fucked.**

AWS 장애 관련 내용을 찾다가 레딧에서 하나 글을 보게 되었는데 여러 댓글이 있었다.

> - AWS 리전 중에서도 의존도가 상당한데 왜 아직까지도 해결 못하고 있는지..
> - 복원력을 극대화하려면 여러 리전 간의 중복이 필요하다.
> - 결국 모든 시스템은 어딘가에 단일 장애 지점이 있다.
> - 그 지역은 저주 받았고 100% 유령 나온다.
> - AWS: 코드 업데이트의 75%를 AI를 사용하고 있습니다.

어찌보면 `US-EAST-1`가 기본 리전이어서 점유율이 가장 높은데 과거에도 피해를 입은 사람들이 대부분인 것 같다.

## [영향 받은 서비스](https://www.linkedin.com/posts/thomaseccel_aws-amazonwebservices-activity-7385962329718276096-XyGV?utm_source=share&utm_medium=member_desktop&rcm=ACoAAC4kePoBhpEwyaexPI2o6yFnLybpfRibMWU)
![image](/images/2025/aws-us-east-1-outage.png)

### *나무위키에 올라온 서비스 목록은 다음과 같다*
<details>
<summary>접기/펼치기</summary>
Airtable,Brightspace,Canva,Docker Hub,Fall Guys,Heroku,Hell Let Loose,Parsec,Perplexity,PlayStation Network,Reddit,Roblox,Samsung Account,Signal,Steam,TIDAL,Udemy,Venmo,Vercel,Pokémon GO,닌텐도 홈페이지,더 파이널스,듀오링고,디즈니+,레인보우 식스 시즈 X,로켓 리그,배틀그라운드,브롤스타즈,스냅챗,슬랙,아마존 뮤직,아마존 알렉사,아마존닷컴,위불,코인베이스,클래시 로얄,죠죠의 기묘한 모험 올 스타 배틀 R,클래시 오브 클랜,페이트 그랜드 오더,헤이데이,붐비치,스쿼드 버스터즈,Mo.co,포트나이트,프라임 비디오,플링,에픽게임즈 스토어,VRChat
</details>

## 조치 과정
> Oct 20 2:22 AM PDT We have applied initial mitigations and we are observing early signs of recovery for some impacted AWS Services. During this time, requests may continue to fail as we work toward full resolution. We recommend customers retry failed requests. While requests begin succeeding, there may be additional latency and some services will have a backlog of work to work through, which may take additional time to fully process

> Oct 20 3:35 AM PDT The underlying DNS issue has been fully mitigated, and most AWS Service operations are succeeding normally now. Some requests may be throttled while we work toward full resolution. Additionally, some services are continuing to work through a backlog of events such as Cloudtrail and Lambda. While most operations are recovered, requests to launch new EC2 instances (or services that launch EC2 instances such as ECS) in the US-EAST-1 Region are still experiencing increased error rates. We continue to work toward full resolution. If you are still experiencing an issue resolving the DynamoDB service endpoints in US-EAST-1, we recommend flushing your DNS caches. We will provide an update by 4:15 AM, or sooner if we have additional information to share.

> Oct 20 4:48 AM PDT We continue to work to fully restore new EC2 launches in US-EAST-1. We recommend EC2 Instance launches that are not targeted to a specific Availability Zone (AZ) so that EC2 has flexibility in selecting the appropriate AZ. The impairment in new EC2 launches also affects services such as RDS, ECS, and Glue. We also recommend that Auto Scaling Groups are configured to use multiple AZs so that Auto Scaling can manage EC2 instance launches automatically.
We are pursuing further mitigation steps to recover Lambda’s polling delays for Event Source Mappings for SQS. AWS features that depend on Lambda’s SQS polling capabilities such as Organization policy updates are also experiencing elevated processing times. We will provide an update by 5:30 AM PDT.

> Oct 20 5:10 AM PDT We confirm that we have now recovered processing of SQS queues via Lambda Event Source Mappings. We are now working through processing the backlog of SQS messages in Lambda queues.

> Oct 20 12:15 PM PDT We continue to observe recovery across all AWS services, and instance launches are succeeding across multiple Availability Zones in the US-EAST-1 Regions. For Lambda, customers may face intermittent function errors for functions making network requests to other services or systems as we work to address residual network connectivity issues. To recover Lambda’s invocation errors, we slowed down the rate of SQS polling via Lambda Event Source Mappings. We are now increasing the rate of SQS polling as we experience more successful invocations and reduced function errors. We will provide another update by 1:00 PM PDT.

> Oct 20 1:03 PM PDT Service recovery across all AWS services continues to improve. We continue to reduce throttles for new EC2 Instance launches in the US-EAST-1 Region that were put in place to help mitigate impact. Lambda invocation errors have fully recovered and function errors continue to improve. We have scaled up the rate of polling SQS queues via Lambda Event Source Mappings to pre-event levels. We will provide another update by 1:45 PM PDT.

### **2:22 AM PDT**
: 초기 완화 조치

### **3:35 AM PDT**
: 근본적인 DNS 완화가 되었지만 복구를 위해 일부 요청은 제한시킴. EC2 생성 요청은 여전히 오류 발생

### **4:48 AM PDT**
: EC2 생성 요청 시 AZ 선택 안함 권장, Auto Scaling 그룹이 여러 AZ 사용하도록 권장

### **5:10 AM PDT**
: Lambda를 통한 SQS 대기열 처리 복구 완료

### **12:15 PM PDT**
: 여러 AZ에서 EC2 생성 완료 확인, Lambda 오류를 복구하기 위해 SQS 폴링 속도 감소

### **1:03 PM PDT**
: EC2 생성 제한 정도 감소, Lambda 호출 오류 복구, SQS 폴링 속도 확장

여기까지가 `AWS Health`에서 보고한 내용이고, 지금은 대부분의 문제는 해결됐을 것 같다.

## 비슷한 사례
### [2018년 AWS 한국 리전 장애](https://aws.amazon.com/ko/blogs/korea/follow-up-to-the-november-22-event-in-aws-seoul-region/)
이번처럼 대규모는 아니고 한국 리전에서만 발생했던 사례지만 장애 원인은 DNS 문제로 유사하다. 이때도 Failover가 되던 기업 외에는 서비스가 중단되어 공지만 하고 AWS에서 복구해주기를 기다렸다고 한다. 로컬 규모라서 그런지 1시간 반만에 해결되었다.

이 사태 이후로 **국내 클라우드(NCP, NHN, KT 등)를 추가 또는 전환**한 기업도 많다고 한다. 아무래도 국내를 대상으로 하니 비슷한 사례가 발생해도 더 빨리 대응할 수 있기 때문이다.

### 2024년 CrowdStrike 전산 마비 사태
클라우드 관련 사태는 아니지만 이런 대규모 사태는 불과 1년 전에도 있었다. 클라우드에 AWS, GCP, Azure가 있듯이 OS는 Windows, Mac이 있는데 여기서 **Windows**의 문제였다.

이거는 DNS가 아니라 문제되는 패치가 배포됐기 때문인데, 이 패치가 적용된 곳은 부팅이 되지 않았다.

## 마무리
여느 때와 비슷하게 링크드인, 긱뉴스에서 사건사고들을 보고 있었는데 우연히 이 사태를 보게 되었다. 왠지 모를 흥미를 갖고 정보를 모아봤는데 단순한 또는 단순하지 않은 오류 하나가 전 세계를 들썩인 것이 신기했다. 원래 잠들려고 했는데 이것 때문에 눈이 번뜩 떠져서 정보를 수집하게 되었다.

### 양날의 검
어느 순간부터 어떤 서비스의 점유율이 높다는 것이 과연 좋기만 한건지 의문을 갖게 되었다. 물론 그 시장에서 우리의 서비스를 더 많이 사용하고 관심을 가져주는 것은 좋은 신호다.

최근 정부 행정망 화재를 비롯하여 과거 22년 카카오 데이터센터 화재 등을 보면 점유율이 높다는 것은 양날의 검인 것 같다. 나도 그 순간에 카카오톡을 사용 중이었는데 메시지 발송이 안됐고, 당시에는 재직중이면서 알림톡 담당이기도 해서 서비스에 영향이 갔는지 확인했었다. 이렇게 대부분의 국민에게 영향을 끼친 카카오는 최근에 UI 변경 및 숏폼 관련 이슈로 또 비판을 많이 받았다.

그런데 나를 포함하여 대중들은 아직도 `카카오톡`을 사용 중이다. 그렇다고 영원히 벗어나지 못할까?

### 근본적인 원인
다시 본론으로 돌아와서 위에서 발생한 문제들을 잘 살펴보면 어떤 조직의 사이버 공격이 아니라 내부 설계/운영의 문제로 발생한 사례들이다. 대체로 이번에 처음 문제가 발생한 사례가 아니다. 이미 과거에 발생했었는데 비슷한 문제로 또 발생했고 아직 해결을 못 한 상황이라고 봐야 할 것이다. 해결하는 게 쉽지는 않겠지만 그렇다고 추후 또다시 발생할 확률이 있는데 아무 조치도 하지 않으면 똑같은 결과 혹은 더 큰 리스크를 떠안게 될 것이다.

일차적으로 비용 문제가 있겠지만 이중화, 가능하다면 멀티 리전도 고려해 볼 수 있다. AWS에 기능이 있는지 모르겠지만 특정 리전에서 장애가 발생했을 때, 다른 리전으로 임시 적용해 줄 수는 없을까?

내부 스펙에 맞게 헬스 체크, TTL 조정 등을 하고 모니터링을 철저히 하는 방법도 있다. 그나마 다행인 것이 이번 모니터링에서 비정상적인 트래픽이 발생한 것을 빠르게 확인해서 초기 조치가 잘 이루어진 것 같다.

> **큰 힘에는 큰 책임이 따른다**

## 입장문 나온 이후 요약
해당 지역 시간 기준 2025년 10월 19일 오후 11시 48분부터 10월 20일 오후 2시 20분까지 경과했다. 장애 원인은 **DynamoDB의 DNS 관리 시스템의 잠재적 Race Condition** 때문에 해당 지역 엔드포인트(dynamodb.us-east-1.amazonaws.com)에 대한 **잘못된 빈 DNS 레코드가 발생**하여 자동화가 복구되지 못했다.

여기에는 **`DNS Planner`**, **`DNS Enactor`** 라는 두 구성 요소가 DynamoDB의 자동 DNS 관리 아키텍처 내에 존재한다. 간단하게 `Planner`는 plan을 생성하고, `Enactor`는 해당 plan을 내부 DNS 서비스에 적용하는 역할을 한다. 그런데 `Enactor`는 예상보다 적용되는 시간이 지연되었고, `Planner`는 계속 plan을 생성했다. 이 과정에서 다른 Enactor는 새로운 plan을 적용한 뒤, "이전 plan은 더 이상 유효하지 않다"는 이유로 클린 작업을 수행했다. 결국 지연된 `Enactor`가 뒤늦게 작업을 마치면서 (older) plan을 적용해버리고, 이전 plan은 클린된 상태여서 DNS 레코드가 빈(empty) 상태로 남는 상황이 발생하게 된다.
> DynamoDB의 리전 엔드포인트(e.g. dynamodb.us-east-1.amazonaws.com)에 대한 IP 주소 레코드가 모두 제거됨

DynamoDB에 접근할 수 없게 되면서 그 데이터 저장소나 상태 저장으로 사용하는 AWS 시스템들이 정상적으로 작동하지 않았다. 대표적으로 NLB의 헬스 체크 실패가 반복되며, `Connection errors`나 `지연`이 증가했다.

향후 대책으로 언급한 것은 위에서 말한 **`DNS Planner`**, **`DNS Enactor`** 자동화 기능을 일시적으로 비활성화하고, 새로운 plan이 이전 plan보다 최신인지 체크하는 로직 등 자동화 DNS 관리 시스템의 설계 및 검증 메커니즘을 강화한다고 한다. **`NLB`** 는 헬스 체크로 AZ 장애가 발생하면 단일 NLB가 제거할 수 있는 용량을 제한하는 속도 제어 메커니즘을 추가한다고 한다. **`EC2`** 는 throttling 메커니즘을 개선하여 대기열의 크기에 따라 들어오는 작업의 속도를 제한시킨다고 한다.

### 공식 입장문
> ... The root cause of this issue was a latent race condition in the DynamoDB DNS management system that resulted in an incorrect empty DNS record for the service’s regional endpoint (dynamodb.us-east-1.amazonaws.com) that the automation failed to repair.

> ... First, the DNS Planner continued to run and produced many newer generations of plans. Second, one of the other DNS Enactors then began applying one of the newer plans and rapidly progressed through all of the endpoints. The timing of these events triggered the latent race condition.

> ... We are making several changes as a result of this operational event. We have already disabled the DynamoDB DNS Planner and the DNS Enactor automation worldwide. In advance of re-enabling this automation, we will fix the race condition scenario and add additional protections to prevent the application of incorrect DNS plans. For NLB, we are adding a velocity control mechanism to limit the capacity a single NLB can remove when health check failures cause AZ failover. For EC2, we are building an additional test suite to augment our existing scale testing, which will exercise the DWFM recovery workflow to identify any future regressions. We will improve the throttling mechanism in our EC2 data propagation systems to rate limit incoming work based on the size of the waiting queue to protect the service during periods of high load.


## 참고 자료
[Thomaseccel](https://www.thomaseccel.com/blogs/news/aws-amazon-web-services-major-outage)  
[AWS Health](https://health.aws.amazon.com/health/status?eventID=arn:aws:health:us-east-1::event/MULTIPLE_SERVICES/AWS_MULTIPLE_SERVICES_OPERATIONAL_ISSUE/AWS_MULTIPLE_SERVICES_OPERATIONAL_ISSUE_BA540_514A652BE1A)   
[Outage Summary](https://aws.amazon.com/ko/message/101925/)   
[Reuters](https://www.reuters.com/business/retail-consumer/amazon-cloud-outage-online-services-hit-recovery-uneven-2025-10-20/)     
[Reddit](https://www.reddit.com/r/aws/comments/1obeozt/how_tf_did_aws_mess_up_so_bad_that_the_entire/)    
[Namuwiki](https://namu.wiki/w/%EC%95%84%EB%A7%88%EC%A1%B4%20%EC%9B%B9%20%EC%84%9C%EB%B9%84%EC%8A%A4#s-6.1.2)