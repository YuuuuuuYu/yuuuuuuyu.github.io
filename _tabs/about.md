---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
---

# 🤔 Who Am I?
---
    저는 문제를 깊이 생각하고 해결책을 찾는 것을 즐깁니다.    
    제 지식의 한계를 인식하고, 다른 팀원들과의 생각을 공유하며    
    새로운 아이디어를 발견하는 것을 선호합니다.

    같은 문제를 다양한 관점에서 바라보면서    
    제 사고가 확장되는 과정에서 큰 성취감을 느낍니다.

    팀원들과 각자의 생각과 관점을 나누어     
    많은 사용자들이 유용하게 사용할 수 있는 소프트웨어를 개발하고 싶습니다.


# 👨‍💼 Career
---
## **파이언넷 (2020. 01 ~ 2024. 07)**
    AK 쇼핑몰 시스템 개발 및 유지보수  
    - 고객, 검색, 업체 서비스 개발 및 유지보수
    - 주문, LMS/알림톡 서비스 개발 및 유지보수
    - 이벤트 서비스 개발 및 유지보수


# 📚 Projects
---
## **파이언넷 (2020. 01 ~ 2024. 07)**
### **- AK몰 서비스 형상 유지 (2024. 03 ~ 2024. 07)**
- AK몰이 `인터파크커머스`에 인수되면서 진행중인 모든 프로젝트가 중단되어 기존 서비스만 유지


### **- 검색 페이지 리뉴얼 (2023. 09 ~ 2024. 02)**
- ##### **배경**
    검색 결과 페이지의 `쿼리 스트링`에 불필요한 정보가 많이 포함되어 있었고, 전체 UI의 개선이 필요.     
    하지만 외부 업체의 검색 솔루션을 사용하고 있어 원하는 방향으로 개선하기 위해서는 추가 비용이 발생.  
    이에 추가 비용 없이 최대한 적용 가능한 범위 내에서 리뉴얼 진행한 프로젝트
- ##### **담당업무 (개발 2명, 기획 2명)**
    \- 검색 결과 필터 로직 개선     
    \- 쿼리스트링 간소화
- ##### **개발과정**
    먼저, 소스 코드가 하나에 집중되어 있어 공통 부분을 분리하였습니다. 카테고리, 브랜드, 가격 등 주요 옵션만 사이드바에 포함시키고, 불필요한 선택 옵션은 최소화하여 적용했습니다.     
    또한, 폼에 담긴 상품 정보를 `GET` 방식에서 `POST` 방식으로 전환하여 필요한 정보만 URL에 포함시켰습니다.
- ##### **성과**
    \- 추가 비용 없이 기존 환경에서 검색 기능과 필터 로직을 효율적으로 적용하는 방안을 모색한 경험이었습니다. 그러나 AK몰이 인수되면서 프로젝트가 중단되어 아쉬움이 남습니다.
- ##### **기술스택**
###### ![badge](https://img.shields.io/badge/Java/Spring-6DB33F?style=flat&logo=spring&logoColor=white) ![badge](https://img.shields.io/badge/JSP--yellow)


### **- 검색 배너/CS 키워드 관리 시스템 개발 (2023. 05 ~ 2023. 08)**
- ##### **배경**
    기존 검색 시스템은 상품 결과와 배너 이미지만 노출. 회원가입, 배송조회 등 CS 키워드를 추가하고, 키워드 클릭 시 FAQ로 이동하도록 기능을 추가하는 프로젝트
- ##### **담당업무 (개발 2명, 기획 2명)**
    \- CS 키워드 테이블, 검색 키워드 메타 테이블 생성  
    \- 전체 검색 키워드 서비스 통합 관리
- ##### **개발과정**
    배너 키워드를 확인해보니 현재 사용되지 않는 테이블과 컬럼이 있었고, CS 키워드를 함께 관리하기 위해 `메타 테이블`이 필요하다는 것을 알게 되었습니다.    
    이에 각 키워드에 공통으로 적용되는 값은 메타 테이블에 추가하고, 개별 특징은 각 키워드 테이블에 넣어 데이터를 `구조화`하였습니다.   
    또한 분석계 데이터를 활용하여 키워드별 ID에 매칭되는 누적 `조회수`와 `클릭수`를 확인할 수 있도록 구현했습니다.
- ##### **성과**
    \- 서로 다른 구조의 테이블을 효과적으로 관리하기 위한 설계와 관리 방안을 고민할 수 있었습니다.   
    \- 자바 8의 기능을 제대로 활용한 적이 없었는데, 이번에 `stream`의 `filter`를 통해 복잡한 로직을 가독성 있게 처리할 수 있었습니다.
- ##### **기술스택**
###### ![badge](https://img.shields.io/badge/Java/Spring-6DB33F?style=flat&logo=spring&logoColor=white) ![badge](https://img.shields.io/badge/Javascript-F7DF1E?style=flat&logo=javascript&logoColor=white) ![badge](https://img.shields.io/badge/Oracle-F80000?style=flat&logo=oracle&logoColor=white) ![badge](https://img.shields.io/badge/Mybatis--red)


### **- 임직원 자동 탈퇴 프로세스 개발 (2023. 02 ~ 2023. 04)**
- ##### **배경**
    퇴사자가 퇴사 후에도 탈퇴되지 않은 계정을 통해 임직원 복지를 악용하는 사례가 발생.  
    주기적으로 퇴사자 정보를 받아 대상자를 자동으로 탈퇴 처리하는 프로젝트
- ##### **담당업무 (개발 2명)**
    \- 탈퇴 대상자 관리 테이블 생성     
    \- 자동 탈퇴 프로세스 개발
- ##### **개발과정**
    퇴사자 정보를 제공하는 API를 통해 `퇴사일자`와 `사번`을 받아올 수 있어, 고객 테이블에 탈퇴 대상자를 체크할 수 있는 컬럼을 추가하면 최소한의 자원으로 처리할 수 있을 것으로 예상했습니다.    
    그러나 퇴사일로부터 15일째 되는 날에 알림을 발송하고, 다시 15일 후에 탈퇴 처리를 해야 하는 것을 체크하고 관리하려면 고객 테이블에 컬럼 하나를 추가하는 것으로는 비효율적이었습니다.     
    따라서 탈퇴 대상자의 `알림 발송 여부`, `탈퇴 여부` 등을 체크할 수 있는 별도의 `테이블을 생성`하여 관리하게 되었습니다. 이후 매일 퇴사일자를 기준으로 데이터를 받아 탈퇴 프로세스가 자동으로 처리되도록 배치를 설정했습니다.
- ##### **성과**
    \- 고객 테이블이 이미 무거워서 단순히 컬럼 하나를 추가하는 것만으로는 비효율적일 수 있다는 것을 깨달았습니다.    
    \- 고객 테이블 데이터가 적고 퇴사자 대상자가 적었다면 다시 고려해볼 수 있었지만, `자원 관리`와 추후 `유지보수` 측면에서 어떻게 처리해야 하는지 고민해볼 수 있는 경험이었습니다.
- ##### **기술스택**
###### ![badge](https://img.shields.io/badge/Java-black?style=flat&logo=openjdk&logoColor=white) ![badge](https://img.shields.io/badge/Oracle-F80000?style=flat&logo=oracle&logoColor=white) ![badge](https://img.shields.io/badge/Jdbc--white)


### **- MD 계약 수수료 자동 세팅 기능 개선 (2022. 12 ~ 2023. 01)**
- ##### **배경**
    MD들이 업체 계약을 진행할 때, 자주 사용하는 수수료율을 매번 `수동`으로 입력해야 하는 번거로움이 발생. 계약을 등록할 때, 각 MD별로 수수료가 `자동`으로 세팅하는 프로젝트
- ##### **담당업무 (개발 1명)**
    \- MD별 계약 수수료 화면 세팅 자동화    
    \- MD별 계약 수수료 등록/수정 관리
- ##### **개발과정**
    각 MD의 최대 수수료율은 `10개로 제한`되어 있으며, MD 수가 수십 명에 달해 전체 데이터는 1,000개 미만으로 예상되었습니다. 이에 별도의 테이블을 생성하지 않고 기존 테이블에서 데이터를 관리하는 것이 효율적이라고 판단하였습니다.  
    `공통 관리 테이블`에 수수료 자동 설정을 위한 키 값을 정의하고, 각 MD의 ID와 여러 수수료율을 저장할 수 있는 규칙을 수립하였습니다. 이후 계약 수수료 등록 및 수정 화면에서 해당 MD의 수수료 자동 설정 값이 존재할 경우 이를 자동으로 반영하도록 구현하였습니다.
- ##### **성과**
    \- MD들의 계약 수수료 등록 및 수정 시간이 이전에 비해 `50%` 단축되었습니다.     
    \- 별도의 테이블을 생성하지 않고 기존 테이블을 활용함으로써 시스템 리소스를 효율적으로 사용하고 유지보수 비용을 절감하였습니다.
- ##### **기술스택**
###### ![badge](https://img.shields.io/badge/Javascript-F7DF1E?style=flat&logo=javascript&logoColor=white) ![badge](https://img.shields.io/badge/Oracle-F80000?style=flat&logo=oracle&logoColor=white) ![badge](https://img.shields.io/badge/Mybatis--red)

### **- 협력업체 관리자 계정 찾기 기능 개발 (2022. 10 ~ 2022. 11)**
- ##### **배경**
    협력업체 담당자가 계정을 분실할 경우 `수동`으로 초기화하는 절차의 불편함을 해소하고, 담당자들이 직접 계정을 찾을 수 있도록 서비스 기능을 추가하는 프로젝트
- ##### **담당업무 (개발 1명, 기획 2명)**
    \- 아이디 찾기 개발   
    \- 비밀번호 찾기 개발
- ##### **개발과정**
    `사업자 번호`와 `대표자명`을 입력받아 일치 여부를 확인한 후, 이메일 또는 문자로 6자리 랜덤 인증번호를 전송하였습니다. `인증번호`는 세션에 저장되며, 5분 후 또는 인증 완료 시 세션에서 제거하여 재사용을 방지하였습니다.   
    인증이 완료되면 아이디 찾기의 경우 일부 아이디를 공개하고, 전체 아이디는 이메일 발송을 통해 확인할 수 있도록 구현하였습니다. 비밀번호 찾기의 경우 새로운 비밀번호를 입력하도록 유도하였습니다.

- ##### **성과**
    \- 담당자들의 계정 관련 문의 건수가 `90%` 감소했습니다.     
    \- `세션` 타임아웃 설정 및 보안 로직 구현을 통해 시스템의 보안성을 강화하였습니다.

- ##### **기술스택**
###### ![badge](https://img.shields.io/badge/Java/Spring-6DB33F?style=flat&logo=spring&logoColor=white) ![badge](https://img.shields.io/badge/Javascript-F7DF1E?style=flat&logo=javascript&logoColor=white) ![badge](https://img.shields.io/badge/Oracle-F80000?style=flat&logo=oracle&logoColor=white) ![badge](https://img.shields.io/badge/Mybatis--red)


### **- 알림톡 템플릿 사이트 문구 변경 (2022. 07 ~ 2022. 09)**
- ##### **배경**
    임직원몰에서 발송되는 모든 알림톡의 사이트 문구를 `임직원몰`에서 `복지몰`로 변경. 그러나 알림톡 발송 경로가 분산되어 있어 유지보수의 효율성을 높이기 위해 일부 공통화가 필요. 
- ##### **담당업무 (개발 1명, 기획 2명)**
    \- 공통 문구를 정적 변수 하나로 통합    
    \- 불필요한 함수 제거 및 공통 로직 통합
- ##### **개발과정**
    대부분의 사이트 문구가 `하드 코딩`되어 있었기 때문에, 재사용성을 높이기 위해 `정적 변수`로 전환하였습니다. 또한, 중복되거나 불필요하게 작성된 함수를 정리하고 공통 로직을 통합하여 코드의 일관성과 효율성을 향상시켰습니다.  
    알림톡 발송은 운영 서버에서만 가능했기 때문에, 먼저 개발 서버에 변경 사항을 적용한 후 각 케이스별 데이터 저장을 검증하고, 순차적으로 운영 서버에 반영하여 서비스의 안정성을 확보하였습니다.
- ##### **성과**
    \- 전체 코드량이 `10%` 감소하여 향후 문구 변경 시 작업 시간을 단축시켰습니다.  
    \- 또한, `설계 단계`에서 유지보수성을 고려한 코드 작성의 필요성을 인식하게 되었습니다.
- ##### **기술스택**
###### ![badge](https://img.shields.io/badge/Java-black?style=flat&logo=openjdk&logoColor=white) ![badge](https://img.shields.io/badge/Oracle-F80000?style=flat&logo=oracle&logoColor=white) ![badge](https://img.shields.io/badge/Mybatis--red)


### **- 샤넬 멤버십 연동 기능 개발 (2022. 03 ~ 2022. 06)**
- ##### **배경**
    자사몰에서 샤넬 상품 주문 시 샤넬 `멤버십과 연동`하여 멤버십 `포인트를 적립`하는 기능을 추가하는 프로젝트
- ##### **담당업무 (개발 3명, 기획 2명)**
    \- 샤넬 상품 주문 시 멤버십 가입 레이어 팝업 활성화   
    \- 샤넬 브랜드 주문 데이터 조회 API 개발
- ##### **개발과정**
    주문 완료 시 샤넬 상품이 포함된 경우 멤버십 연동 팝업을 표시하고, 팝업 클릭 시 고객 정보를 기반으로 샤넬 멤버십 가입을 구현했습니다.    
    또한, `배송완료일자`를 기준으로 샤넬 상품 주문 내역을 조회하는 API를 제공하여 샤넬이 주기적으로 포인트를 적립할 수 있도록 지원했습니다.  
    외부 업체와의 협업 과정에서 `실무 용어`<sup>[a](#footnote_a)</sup> 와 `배포 일정`의 차이를 극복하며 원활한 의사소통을 이루었습니다.    
    ><a name="footnote_a">a</a>: SIT, UAT 등 테스트 용어
- ##### **성과**
    \- 포인트 적립 프로세스 자동화를 통해 샤넬 상품 구매를 유도하고 새로운 커뮤니케이션 용어를 익히며 외부 협업 능력을 향상시켰습니다.     
    \- 협업 도구의 중요성을 인식하여 향후 `Slack`과 같은 실시간 소통 도구를 도입하여 협업 효율성을 더욱 높일 계획입니다.

- ##### **기술스택**
###### ![badge](https://img.shields.io/badge/Java/Spring-6DB33F?style=flat&logo=spring&logoColor=white) ![badge](https://img.shields.io/badge/Javascript-F7DF1E?style=flat&logo=javascript&logoColor=white) ![badge](https://img.shields.io/badge/JSP--yellow) ![badge](https://img.shields.io/badge/Mybatis--red)


### **- 적립금 지급 안내 알림 배치 개발 (2022. 01 ~ 2022. 02)**
- ##### **배경**
    기존 시스템에서는 특정 프로모션을 통한 적립금 지급 시에만 알림이 발송되었으나, 이벤트 적립금의 경우 지급에도 불구하고 고객이 이를 인지하지 못하는 사례가 많았습니다. 이를 개선하기 위해 이벤트 적립금 지급 시 자동으로 알림톡을 발송하는 기능을 추가하는 프로젝트
- ##### **담당업무 (개발 1명, 기획 1명)**
    \- 이벤트 적립금 지급 시 알림톡 발송
- ##### **개발과정**
    알림톡 서버의 트래픽이 높은 상황에서 실시간 발송을 허용하면 서버 과부하가 발생할 수 있습니다. 이를 해결하기 위해 적립금 지급 시점이 아닌 특정 시간대에 알림톡을 `일괄 발송`하도록 시스템을 설정하여 서버 부하를 분산시켰습니다.   
    당일 적립금이 지급된 고객을 대상으로 이벤트명, 적립금액을 포함하여 알림톡으로 발송하는 로직을 구현하였습니다.  
    특히, 적립금 지급은 주로 오후 시간대에 이루어지고 퇴근 시간대에 서버 유입률이 증가하는 점을 고려하여 오후 5시에서 6시 사이에 발송되도록 배치 작업을 설정하였습니다.
- ##### **성과**
    \- 알림톡 발송을 통해 고객의 적립금 인지율을 높여서 서버 유입률을 `20%` 증가시켰습니다.  
    \- 또한, 업무별 배치 시간이 겹치지 않도록 조정하여 다른 배치 작업과의 충돌을 최소화하고, 전체 시스템의 안정성을 유지하였습니다.

- ##### **기술스택**
###### ![badge](https://img.shields.io/badge/Java-black?style=flat&logo=openjdk&logoColor=white) ![badge](https://img.shields.io/badge/Oracle-F80000?style=flat&logo=oracle&logoColor=white) ![badge](https://img.shields.io/badge/Jdbc--white)


### **- 메시지 발송 성능 개선 (2021. 07 ~ 2021. 12)**
- ##### **배경**
    대량 메시지 발송 시, 인증번호나 주문 완료 메시지와 같은 실시간 메시지들이 `지연`되는 문제가 발생. 실시간 메시지의 즉시 발송을 보장하기 위해 성능 `개선`을 진행한 프로젝트
- ##### **담당업무 (개발 2명, 기획 2명)**
    \- LMS 및 알림톡 발송 쿼리 최적화 수행  
    \- LMS/알림톡 에이전트의 `idle` 개수 증대 작업
- ##### **개발과정**
    기존 쿼리에 `인덱스`가 제대로 적용되지 않아 효율성이 저하되었고, 실시간 메시지와 일반 메시지가 동일한 스레드에서 처리하여 메시지 발송이 `지연`되었습니다.   
    이를 해결하고자, 힌트를 추가해 인덱스를 수정하여 쿼리 성능을 최적화하고, 실시간 메시지와 일반 메시지를 분리하기 위해 별도의 `스레드를 추가`했습니다. 실시간 메시지 스레드에 `우선순위`를 적용하여, 다른 메시지와 동시에 큐에 들어가더라도 먼저 발송되도록 설정했습니다.    
    또한, 발송 대기 건수를 실시간으로 확인할 수 있는 스레드를 추가하여 전체 발송 상황을 모니터링 가능하게 했습니다.
- ##### **성과**
    \- 알림톡의 월 평균 성공률이 `85%`에서 `95%`로 향상시켰습니다.  
    \- 마케팅 문자 발송 속도를 10분당 1만 건에서 2만 건으로 `2배` 개선하여 발송 처리 효율을 크게 향상시켰습니다.

- ##### **기술스택**
###### ![badge](https://img.shields.io/badge/Java-black?style=flat&logo=openjdk&logoColor=white) ![badge](https://img.shields.io/badge/Oracle-F80000?style=flat&logo=oracle&logoColor=white) ![badge](https://img.shields.io/badge/Jdbc--white)


### **- 이벤트 시스템 개발 및 관리 (2020. 05 ~ 2021. 06)**
- ##### **배경**
    매주 1~2회 담당 기획자와 비정형 이벤트 진행
- ##### **담당업무 (개발 2명, 기획 2명)**
    \- 비정형 이벤트 서비스 개발    
    \- 정형 이벤트 서비스 관리
- ##### **개발과정**
    출석체크, 페이백 이벤트 등 `정형` 이벤트 외에도 추천인 가입, 선착순 주문, 랜덤 쿠폰 다운로드 등 다양한 `비정형` 이벤트를 개발했습니다. 비정형 이벤트는 각 이벤트의 `설정`(확률, 횟수 등)에 따라 타입을 분류하여 관리하였습니다.  
    `추천인 가입` 이벤트에서는 신규 가입자를 대상으로 추천받은 계정을 누적 카운트해야 했습니다. 이에 추천받은 계정마다 카운트를 합산할지, 추천을 받을 때마다 데이터를 저장하고 화면에 노출하기 전에 합산할지 고민하였습니다. 해당 이벤트가 단기간에 끝나는 것이 아니고 `동시성` 문제로 인한 트래픽 영향이 크지 않을 것으로 판단하여 전자의 방법을 선택하였습니다.     
    `선착순 주문` 이벤트는 이벤트 시간대별로 현재 시간과 비교하여 이미지를 활성화하고, 품절 상품이나 오픈 전 상품의 경우 비활성화하였습니다.   
    `랜덤 쿠폰 다운로드`에서는 이벤트 테이블에서 확률 구간을 정하고 각 구간마다 쿠폰 다운로드 링크를 삽입했습니다. 고객은 랜덤으로 나온 값과 매칭되는 쿠폰을 받게 되며, 해당 쿠폰에 횟수 제한이 있어 소진된 경우, 기본 쿠폰을 발급하도록 설정하였습니다.
- ##### **성과**
    \- 다양한 이벤트 서비스의 개발과 테스트를 통해 커머스 시스템의 전반적인 프로세스를 경험하였습니다.     
    \- 비정형 이벤트를 설정에 따라 타입별로 분류하고 관리함으로써 이벤트 개발과 운영의 효율성을 향상시켰습니다.
- ##### **기술스택**
###### ![badge](https://img.shields.io/badge/Java/Spring-6DB33F?style=flat&logo=spring&logoColor=white) ![badge](https://img.shields.io/badge/Javascript-F7DF1E?style=flat&logo=javascript&logoColor=white) ![badge](https://img.shields.io/badge/JSP--yellow) ![badge](https://img.shields.io/badge/Oracle-F80000?style=flat&logo=oracle&logoColor=white) ![badge](https://img.shields.io/badge/Mybatis--red)


## **사이드 프로젝트**
### **- ITSM 메일 알림 발송 서비스 (2024. 06)**
- ##### **배경**
    고객사가 인수되면서 메신저가 `그룹웨어`에서 `Teams`로 변경되었고, 기존 메일 계정은 사용불가.    
    기존에는 ITSM 접수 건이 있을 때 사용자에게 메일로 알림이 발송되었지만, ITSM 시스템은 그대로 유지된 채 메신저만 변경되면서 메일 알림 기능이 중단된 상황. 이 부족한 부분을 보완하기 위한 프로젝트.
- ##### **담당업무**
    \- 메일 알림 배치 쉘 스크립트 개발
- ##### **개발과정**
    가장 중점적으로 고려한 요소는 `비용`과 `접근성`이었습니다. 팀 내부에서만 사용할 목적이었기 때문에 비용이 들지 않는 방법이 필요했고, 어떤 환경에서도 원활하게 작동할 수 있어야 했습니다.     
    다양한 방법을 검토한 결과, `Outlook API`는 매번 인증 절차가 필요하고, `파이썬`으로 개발할 경우 파이썬이 설치된 환경이 요구되므로 의존도가 가장 낮은 `쉘 스크립트`를 사용하여 개발하기로 결정했습니다.   
    `JSESSIONID` 값을 이용해 ITSM 접수 건수를 조회하는 URL이 있는데, 해당 값이 0보다 클 때 메일이 발송되도록 설정했습니다. `ChatGPT`를 통해 쉘 스크립트를 기본적으로 구현하고, 세부적인 부분은 직접 수정하여 최적화했습니다.
- ##### **성과**
    배치 시간 조절 기능을 추가하여 실시간 알림이 필요한 사용자와 그렇지 않은 사용자를 모두 만족시킬 수 있었습니다. 메일 발송과 접근성 문제에 대해 각 팀원의 스타일을 맞추며 깊이 있게 고민하고 해결할 수 있었던 좋은 경험이었습니다.
- ##### **링크**
    <a href="https://woorimail.com/" target="_blank">우리메일</a>   
    <a href="https://yuuuuuuyu.github.io/posts/woorimail-api/" target="_blank">소스코드</a>

# ✏️ Skill
---
### **Languages**
###### ![badge](https://img.shields.io/badge/Java-black?style=flat&logo=openjdk&logoColor=white) ![badge](https://img.shields.io/badge/Javascript-F7DF1E?style=flat&logo=javascript&logoColor=white) ![badge](https://img.shields.io/badge/Oracle-F80000?style=flat&logo=oracle&logoColor=white) 

### **Framework**
###### ![badge](https://img.shields.io/badge/Spring-6DB33F?style=flat&logo=spring&logoColor=white) ![badge](https://img.shields.io/badge/SpringBoot-6DB33F?style=flat&logo=springboot&logoColor=white) ![badge](https://img.shields.io/badge/Mybatis--CD0000?style=flat)

### **DevOps**
###### ![badge](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonwebservices&logoColor=white)

### **Communication**
###### ![badge](https://img.shields.io/badge/Groupware-003c83) ![badge](https://img.shields.io/badge/Teams-5255aa)

### **Once I used**
###### ![badge](https://img.shields.io/badge/C++-00599C?style=flat&logo=cplusplus&logoColor=white) ![badge](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![badge](https://img.shields.io/badge/Typescript-3178C6?style=flat&logo=typescript&logoColor=white) ![badge](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white) ![badge](https://img.shields.io/badge/Node.js-5FA04E?style=flat&logo=nodedotjs&logoColor=white)
###### ![badge](https://img.shields.io/badge/Hibernate-59666C?style=flat&logo=hibernate&logoColor=white)  
###### ![badge](https://img.shields.io/badge/GCP-4285F4?style=flat&logo=googlecloud&logoColor=white) ![badge](https://img.shields.io/badge/Bigquery-669DF6?style=flat&logo=googlebigquery&logoColor=white)

# 📃 Education
---
### **강원대학교(2014. 03 ~ 2020. 02)**     
#### **컴퓨터정보통신공학과**


# 🛠 Certifications
---
### **정보처리기사(2019.08)**

