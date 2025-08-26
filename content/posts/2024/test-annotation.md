---
title: 테스트 도구는 어떤게 있을까?
author: nakji
date: 2024-12-18 12:13:00 +0900
tags: [test, mock, junit, gwt]
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
🔔 **테스트 도구 JUnit, Mockito**   
🔔 **테스트 시나리오 작성, GWT**

## **JUnit**
### **@Test**
해당 메서드가 테스트 메서드임을 나타냅니다.
```java
@Test 
void myTest() { /* 테스트 로직 */ }
```

### **@BeforeEach**
각 테스트 메서드가 실행되기 전에 실행되는 메서드를 지정합니다.
```java
@BeforeEach 
void setUp() { /* 초기화 로직 */ }
```

### **@AfterEach**
각 테스트 메서드가 실행된 후에 실행되는 메서드를 지정합니다.
```java
@AfterEach 
void tearDown() { /* 정리 로직 */ }
```

### **@BeforeAll**
모든 테스트 메서드가 실행되기 전에 한 번만 실행되는 메서드를 지정합니다. 정적 메서드이어야 합니다.
```java
@BeforeAll 
static void initAll() { /* 초기화 로직 */ }
```

### **@AfterAll**
모든 테스트 메서드가 실행된 후에 한 번만 실행되는 메서드를 지정합니다. 정적 메서드이어야 합니다.
```java
@AfterAll 
static void tearDownAll() { /* 정리 로직 */ }
```

### **@DisplayName**
테스트 클래스나 메서드의 이름을 지정하여 가독성을 높입니다.
```java
@Test 
@DisplayName("네이버 검색 API 성공 테스트") 
void test() { /*...*/ }
```

## **Mockito**
### **@Mock**
-   **설명**: Mockito에서 제공하는 어노테이션으로, 단순히 모의 객체를 생성합니다.
-   **사용 용도**: 주로 순수한 단위 테스트(Unit Test)에서 사용됩니다. 스프링 컨텍스트와는 별개로 동작합니다.

```java
@RunWith(MockitoJUnitRunner.class)
public class MyServiceTest {
    @Mock
    private DependencyService dependencyService;

    @InjectMocks
    private MyService myService;

    // 테스트 메서드들
}
```

### **@MockBean**
-   **설명**: Spring Boot의 테스트 지원 어노테이션으로, 스프링 애플리케이션 컨텍스트 내의 빈(Bean)을 모의 객체로 대체합니다.
-   **사용 용도**: 스프링 통합 테스트(Integration Test)나 스프링 부트의 애플리케이션 컨텍스트를 사용하는 테스트에서 주로 사용됩니다.
-   **특징**:
    -   스프링의 `ApplicationContext`에 존재하는 실제 빈을 모의 객체로 교체합니다.
    -   스프링의 의존성 주입(Dependency Injection) 메커니즘과 통합되어 동작합니다.

```java
@SpringBootTest
public class MyServiceIntegrationTest {
    @MockBean
    private DependencyService dependencyService;

    @Autowired
    private MyService myService;

    // 테스트 메서드들
}
```

### **@InjectMocks**
-   **설명**: Mockito에서 제공하는 어노테이션으로, `@Mock` 또는 `@Spy`로 생성된 모의 객체들을 주입하여 테스트 대상 객체를 생성합니다.
-   **사용 용도**: 주로 단위 테스트에서 테스트 대상 객체에 의존성을 주입할 때 사용됩니다.
-   **특징**:
    -   생성자, 세터, 필드 주입 방식을 자동으로 처리합니다.
    -   `@Mock`으로 생성된 모든 모의 객체들을 주입합니다.

```java
@RunWith(MockitoJUnitRunner.class)
public class MyServiceTest {
    @Mock
    private DependencyService dependencyService;

    @InjectMocks
    private MyService myService;

    // 테스트 메서드들
}
```

## **추가 어노테이션**
### **@Spy**
-   **설명**: 실제 객체를 스파이(부분 모의 객체)로 감쌉니다. 일부 메서드는 실제로 호출하고, 특정 메서드만 모의할 수 있습니다.
-   **사용 용도**: 부분적으로 동작을 변경하고 싶을 때 유용합니다.
```java
@Spy
private List<String> spyList = new ArrayList<>();
```

### **@Captor**
-   **설명**: ArgumentCaptor를 간편하게 사용하기 위한 어노테이션입니다. 메서드 호출 시 전달된 인자를 캡처할 수 있습니다.
-   **사용 용도**: 특정 메서드가 호출될 때 전달된 인자를 검증하고 싶을 때 사용합니다.
```java
@Captor
ArgumentCaptor<String> captor;
```

### **@ExtendWith(MockitoExtension.class) (JUnit 5)**
-   **설명**: JUnit 5에서 Mockito 어노테이션을 활성화하기 위한 확장 기능입니다.
-   **사용 용도**: JUnit 5 환경에서 Mockito 어노테이션을 사용하려면 필요합니다.
```java
@ExtendWith(MockitoExtension.class)
public class MyServiceTest {
    @Mock
    private DependencyService dependencyService;

    @InjectMocks
    private MyService myService;

    // 테스트 메서드들
}
```

### **Mock vs Spy**
-   **@Mock**:
    -   객체의 모든 메서드를 모의(Mock)합니다.
    -   실제 메서드 호출이 일어나지 않으며, 기본값이 반환됩니다.
-   **@Spy**:
    -   객체의 일부 메서드는 실제로 호출하고, 나머지는 모의(Mock)합니다.
    -   부분적으로 동작을 변경하고 싶을 때 유용합니다.

## **Given-When-Then 패턴**
GWT 패턴은 테스트의 구조를 `Given`, `When`, `Then`으로 나누어 명확하게 테스트 시나리오를 작성하는 방식입니다. Mockito의 어노테이션을 활용하면 각 단계에서 필요한 모의 객체를 손쉽게 설정할 수 있습니다.

-   **Given**:
    -   테스트의 사전 조건을 설정합니다. 예를 들어, 모의 객체의 동작을 정의하거나 초기 데이터를 준비합니다.
    -   `@Mock`, `@MockBean`
-   **When**:
    -   테스트 대상 메서드를 호출합니다.
-   **Then**:
    -   메서드 호출 후의 결과나 상태를 검증합니다.
    -   `@Captor`, `verify`
