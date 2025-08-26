---
title: 4D4cat) 네이버 로그인 연동을 위한 MVC 테스트 1
author: nakji
date: 2024-12-23 22:33:00 +0900
tags: [project, 4d4cat, test, mockito, oauth]
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
🔔 **MVC Test 코드 작성**   

**네이버 연동 페이지에 접근이 잘 되는가?**

## **LoginController.java**
```java
@Controller  
@RequiredArgsConstructor  
@RequestMapping("/login")  
public class LoginController {  
    private final NaverLoginService naverLoginService;  
  
    @GetMapping("/naver")  
    public void naverLogin(HttpServletResponse response) throws IOException {  
        response.sendRedirect(naverLoginService.getNaverOauth2LoginUrl());  
    }  
}
```
### naverLogin
`{URL}/login/naver`로 접근하면 Naver 로그인 인증을 위한 페이지로 이동된다.  
리다이렉트 URL은 `naverLoginService`에서 받는다.


## **NaverLoginService.java**
```java
@Service  
@RequiredArgsConstructor  
public class NaverLoginService {  
    private static final String BASE_URL = "https://nid.naver.com/oauth2.0";  
  
    private final AppProperties app;  
    private final ThirdPartyProperties secrets;  
  
    public String getNaverOauth2LoginUrl() {  
        String authorizeUrl = BASE_URL+"/authorize";  
        String callbackUrl = getServiceUrl()+"/login/naver/callback";  
  
        return UriComponentsBuilder  
                .fromHttpUrl(authorizeUrl)  
                .queryParam("response_type", "code")  
                .queryParam("client_id", secrets.naver().naverId())  
                .queryParam("redirect_uri", callbackUrl)  
                .queryParam("state", "random")  
                .toUriString();  
    }  
    
    public String getServiceUrl() {  
        return app.serviceUrl();  
    }  
}
```
### AppProperties
현재는 도메인 URL만 세팅되어 있다.     
- 로컬 서버 `http://localhost`
- 운영 서버 `https://4d4cat.site`

### ThirdPartyProperties
네이버 포함 여러 서드파티의 키값이 세팅되어 있다.   
여기서는 네이버 `Client_ID` 값이 사용되었다.


## **LoginControllerTest**
```java
@WebMvcTest(LoginController.class)  
@EnableConfigurationProperties({AppProperties.class, ThirdPartyProperties.class})  
@ActiveProfiles("local")  
class LoginControllerTest {  
    @Autowired  
    private AppProperties app;  

    @Autowired  
    private ThirdPartyProperties secrets;  

    @Autowired  
    private MockMvc mockMvc;  

    @MockBean  
    private NaverLoginService naverLoginService;  

    @Nested  
    @DisplayName("네이버 로그인 컨트롤러 테스트")  
    class naverLoginTest {  
        @Test  
        @DisplayName("로컬 URL 정상적으로 적용되는가?")  
        void testServiceUrl_Local() {  
            String serviceUrl = app.serviceUrl();  
            assertNotNull(serviceUrl);  
            assertTrue(serviceUrl.startsWith("http://localhost"), "localUrl: localhost");  
        }  

        @Test  
        @DisplayName("GET /login/naver 정상적으로 접근되는가?")  
        void testNaverLoginPageAccess() throws Exception{  
            String baseUrl = app.serviceUrl();  
            String expectedRedirectUrl = "https://nid.naver.com/oauth2.0/authorize" +  
                    "?client_id="+secrets.naver().naverId()  
                    + "&redirect_uri="+baseUrl+"/login/naver/callback"  
                    + "&response_type=code";  

            when(naverLoginService.getNaverOauth2LoginUrl()).thenReturn(expectedRedirectUrl);  

            mockMvc.perform(get("/login/naver"))  
                    .andExpect(status().is3xxRedirection())  
                    .andExpect(redirectedUrlPattern("https://nid.naver.com/**"))  
            ;  
        }  
    }  
}
```
네이버 로그인 인증 URL이 정상적으로 접근되는지 테스트하는 코드만 있지만, 추후 테스트를 그룹화 하기 위해 `@Nested`로 구분하였다.     
그리고 로컬 환경을 세팅할 때 로컬 도메인이 제대로 적용됐는지, 해당 도메인으로 `redirect_uri` 값이 들어가는지 테스트하는 코드를 작성하였다.
다음 테스트는 인증 이후 토큰을 발급, 갱신하는 테스트를 작성해볼 예정이다.

### @WebMvcTest
LoginController와 관련된 Bean만 로드하여 테스트를 진행

### @EnableConfigurationProperties
환경설정 클래스인 `AppProperties`와 `ThirdPartyProperties`를 사용하기 위해 세팅

### @ActiveProfiles
현재는 `local` 환경에서 테스트를 진행한다.

### when
when(naverLoginService.getNaverOauth2LoginUrl()).thenReturn(expectedRedirectUrl);   
`getNaverOauth2LoginUrl()`가 호출될 때, `expectedRedirectUrl`에 초기화된 값을 반환


## **다른 고민**
- 네이버 로그인 토큰 발급 유형의 grant_type을 미리 enum에 만들어서 관리하면 어떨까?
- 접근 테스트 외에 서비스 단위로 테스트하는 코드를 작성하려면 어디부터 작성해야할까?