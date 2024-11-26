---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
---

# 🤔 Who Am I?
---
    저는 문제를 깊이 생각하고 해결책을 찾는 것을 즐깁니다.

    같은 문제를 다양한 관점에서 바라보고    
    제 사고가 확장되는 과정에서 큰 성취감을 느낍니다.


# 👨‍💼 Career
---
## **파이언넷 (2020. 01 ~ 2024. 07)**
- **AK 쇼핑몰 시스템 개발 및 유지보수**

#### **1. 검색 배너/CS 키워드 관리 시스템 개발**
- 검색 키워드를 메타 테이블을 활용하여 통합 관리함으로써 **고객의 검색 편의성 20% ↑**
- 통합 검색 키워드의 누적 조회수와 클릭수를 제공하여 **현업의 업무 처리 속도 30% ↑**

#### **2. 샤넬 멤버십 포인트 적립 기능 개발**
- 샤넬 주문 데이터 조회 API를 통해 샤넬 측에서 주기적으로 멤버십 포인트 적립
- **샤넬 상품 구매 전환율 10% ↑**

#### **3. 메시지 발송 성능 개선**
- LMS/알림톡 발송 쿼리의 힌트를 최적화하여 **월 평균 발송 성공률 10% ↑**(약 85% -> 95%)
- 발송 에이전트의 스레드를 추가하여 **10분당 처리 건수를 2배 ↑**(약 1만 건 -> 2만 건)

#### **4. 퇴사자 계정 자동 탈퇴 프로세스 개발**
- 퇴사 후 복지 혜택의 악용을 방지하기 위해 퇴사자의 계정을 자동으로 탈퇴하는 프로세스를 개발
- 퇴사자 구분 값을 고객 테이블에 컬럼을 추가하는 대신, 별도의 테이블을 생성하여 **유지보수성 향상**
- 프로세스 적용 이후 **악용 사례를 100% 방지**

#### **5. ITSM 메일 알림 발송 대체 서비스 개발**
- 사내 메신저 교체로 기존 ITSM 알림 메일 기능이 사라져서 대체 서비스를 개발
- 팀 내에서만 사용할 서비스로, 무료 발송이 가능한 WOORIMAIL을 사용하여 **비용 절약**
- ChatGPT를 사용하여 쉘 스크립트 기반 배치 서비스로 **접근성 및 편의성 확보**
- <a href="https://yuuuuuuyu.github.io/posts/woorimail-api/" target="_blank">소스코드</a>


# 📚 Projects
---
## **파이언넷 (2020. 01 ~ 2024. 07)**

### **1. 검색 배너/CS 키워드 관리 시스템 개발 (2023. 05 ~ 2023. 08)**
- #### **AS-IS**
    - 상품 결과와 브랜드 배너 이미지만 노출

- #### **TO-BE**
    - 회원가입, 배송조회 등 CS 키워드 검색 기능 추가
    - 백오피스에서 통합 키워드 관리 화면 구축

- #### **담당업무 (백엔드 2명, 기여도 80%)**
    - CS 키워드 테이블, 검색 키워드 메타 테이블 생성
    - 통합 검색 키워드 관리 화면 구축

- #### **과정**
    1) 배너 키워드를 확인해보니 현재 사용되지 않는 테이블과 컬럼이 있었고, CS 키워드를 함께 관리하기 위해 메타 테이블이 필요하다는 것을 알게 되었습니다.

    2) 각 키워드에 공통으로 적용되는 값은 메타 테이블에 추가하고, 키워드별 특징은 각 키워드 테이블에 넣어 데이터를 구조화하였습니다.

    3) 백오피스에서 관리하는 화면은 메타 테이블 데이터를 활용한 CRUD 작업을 할 수 있도록 구현했습니다.

    4) 또한, 분석계 데이터를 활용하여 각 키워드에 매칭되는 누적 조회수와 클릭수를 추가하여 현업들이 통계 데이터를 실시간으로 조회할 수 있도록 구현했습니다.

- #### **결과**
    - 메타 테이블을 활용하여 키워드를 통합 관리를 함으로써 **고객의 검색 편의성 20% ↑**
    - 통합 검색 키워드의 누적 조회수와 클릭수를 제공함으로써 **현업의 업무 처리 속도 30% ↑**

- #### **기술스택**
###### ![badge](https://img.shields.io/badge/Java/Spring-6DB33F?style=flat&logo=spring&logoColor=white) ![badge](https://img.shields.io/badge/Javascript-F7DF1E?style=flat&logo=javascript&logoColor=white) ![badge](https://img.shields.io/badge/Oracle-F80000?style=flat&logo=oracle&logoColor=white) ![badge](https://img.shields.io/badge/Mybatis--red)

### **2. 샤넬 멤버십 연동 기능 개발 (2022. 03 ~ 2022. 06)**
- #### **AS-IS**
    - 주문 완료 시 별도의 팝업 없음

- #### **TO-BE**
    - 자사몰에서 샤넬 상품 주문 시 샤넬 멤버십과 연동하여 멤버십 포인트를 적립하는 기능 추가

- #### **담당업무 (백엔드 2명, 기여도 70%)**
    - 샤넬 상품 주문 시 주문 완료 페이지에 멤버십 가입 레이어 팝업 추가
    - 샤넬 브랜드 주문 데이터 조회 API 개발

- #### **과정**
    1) 주문 완료 시 상품 브랜드ID를 조회하여 샤넬 상품이 포함된 경우 멤버십 연동 팝업을 노출시켰습니다.

    2) 이후, 팝업을 클릭하면 AK몰 고객 정보를 기반으로 샤넬 멤버십 가입 페이지로 리다이렉트됩니다.

    3) 샤넬 측이 주기적으로 샤넬 상품 주문 내역을 조회할 수 있도록 API를 제공했고, 이는 배송완료일자 기준으로 포인트를 적립할 수 있도록 지원합니다.

- #### **결과**
    - 샤넬 주문 데이터 조회 API를 통해 샤넬 측에서 주기적으로 멤버십 포인트 적립
    - **샤넬 상품 구매 전환율 10%↑**

- #### **기술스택**
###### ![badge](https://img.shields.io/badge/Java/Spring-6DB33F?style=flat&logo=spring&logoColor=white) ![badge](https://img.shields.io/badge/Javascript-F7DF1E?style=flat&logo=javascript&logoColor=white) ![badge](https://img.shields.io/badge/JSP--yellow) ![badge](https://img.shields.io/badge/Mybatis--red)

### **3. 메시지 발송 성능 개선 (2021. 07 ~ 2021. 12)**
- #### **AS-IS**
    - 대량 메시지 발송 시, 인증번호나 주문 완료 메시지와 같은 실시간 메시지 발송 지연

- #### **TO-BE**
    - 실시간 메시지의 즉시 발송 보장

- #### **담당업무 (백엔드 2명, 기여도 80%)**
    - LMS/알림톡 발송 쿼리 힌트 변경
    - LMS/알림톡 에이전트의 스레드 추가

- #### **과정**
    1) 기존 발송 쿼리에 인덱스가 제대로 적용되지 않아 효율성이 저하되었고, 실시간 메시지와 일반 메시지가 동일한 스레드 안에서 처리되어 메시지 발송이 지연되었습니다.

    2) 이를 해결하고자, 적절한 인덱스가 적용되도록 힌트를 수정하여 쿼리 성능을 최적화하고, 실시간 메시지와 일반 메시지 발송을 분리하기 위해 별도의 스레드를 추가했습니다.

    3) 실시간 메시지가 발송되는 스레드에는 우선순위를 적용하여, 일반 메시지와 동시에 메시지 발송 큐에 들어가더라도 우선으로 발송되도록 설정했습니다.

    4) 또한, 발송 대기 건수를 실시간으로 확인할 수 있는 스레드도 추가하여 특정 건수 이상의 대기 건수가 발생 시 알림을 받을 수 있도록 적용했습니다.

- #### **결과**
    - **월 평균 발송 성공률 10% ↑**(약 85% -> 95%)
    - **10분당 발송 처리 건수를 2배 ↑**(10분당 약 1만 건 -> 2만 건)

- ##### **기술스택**
###### ![badge](https://img.shields.io/badge/Java-black?style=flat&logo=openjdk&logoColor=white) ![badge](https://img.shields.io/badge/Oracle-F80000?style=flat&logo=oracle&logoColor=white) ![badge](https://img.shields.io/badge/Jdbc--white)


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
#### **컴퓨터공학과**


# 🛠 Certifications
---
### **정보처리기사(2019.08)**

