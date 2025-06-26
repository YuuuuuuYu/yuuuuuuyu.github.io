---
title: 스프링 시큐리티 기본
author: nakji
date: 2024-12-20 17:50:00 +0800
tags: [spring, security]
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
🔔 **스프링 시큐리티 개념**   

> [스프링 가이드](https://spring.io/guides/gs/securing-web)를 참고하여 스프링 시큐리티의 기본을 공부해보았다.

## **WebSecurityConfig**
```java
@Configuration
@EnableWebSecurity
public class WebSecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        RequestCache nullRequestCache = new NullRequestCache();
        http
                .requestCache((cache) -> cache
                        .requestCache(nullRequestCache)
                )
                .authorizeHttpRequests((requests) -> requests
                        .requestMatchers("/", "/home").permitAll()
                        .anyRequest().authenticated()
                )
                .formLogin((form) -> form
                        .loginPage("/login")
                        .permitAll()
                )
                .logout((logout) -> logout.permitAll());

        return http.build();
    }

    @Bean
    public UserDetailsService userDetailsService() {
        UserDetails user =
                User.withDefaultPasswordEncoder()
                        .username("user")
                        .password("password")
                        .roles("USER")
                        .build();

        return new InMemoryUserDetailsManager(user);
    }
}
```
`@EnableWebSecurity`를 설정하여 시큐리티를 활성화시키고 `securityFilterChain`와 `userDetailsService`를 구현했다.

`securityFilterChain`는 어떤 경로를 보안 설정할지 보여준다. 여기서는 '/'와 '/home' 경로는 인증이 필요하지 않고 나머지 경로에 대해서만 인증을 받도록 설정했다. 인증이 필요한 페이지는 사용자가 성공적으로 로그인하면 이전에 요청한 페이지로 리다이렉션된다. 첫 번째에 `RequestCache`가 선언되어있는데 자세한건 다음 섹션을 참고하길 바란다.  
여기서는 `RequestCache`를 적용하지 않기 위해 `NullRequestCache`를 사용했다.

`userDetailsService`는 사용자명(user), 비밀번호(password), 역할(USER)을 갖는 유저를 하나 생성한다. 이것을 `InMemoryUserDetailsManager`를 통해 in-메모리에 저장하게 된다.


### **continue parameter?**
*In Spring Security 5, the default behavior is to query the saved request on every request. This means that in a typical setup, that in order to use the RequestCache the HttpSession is queried on every request.*

*In Spring Security 6, the default is that RequestCache will only be queried for a cached request if the HTTP parameter continue is defined. This allows Spring Security to avoid unnecessarily reading the HttpSession with the RequestCache.*

*In Spring Security 5 the default is to use HttpSessionRequestCache which will be queried for a cached request on every request. If you are not overriding the defaults (i.e. using NullRequestCache), then the following configuration can be used to explicitly opt into the Spring Security 6 behavior in Spring Security 5.8:*

*RequestCache Only Checks for Saved Requests if continue Parameter Present*

인증이 필요한 리소스에 대해 인증 성공 후 다시 요청하려면 해당 리소스에 대한 요청을 저장할 필요가 있다. 이 때 사용하는 것이 `RequestCache`이다.
위 내용은 `RequestCache`에 대해 스프링 시큐리티 5 버전과 6 버전에서의 적용하는 차이를 알려준다.     
스프링 시큐리티 5 버전에서는 `RequestCache`가 적용되는 **모든 요청에 저장**을 하는 반면, 6 버전에서는 `continue` 같은 **명시적인 파라미터가 들어간 경우**에만 동작하도록 제한되어 있다.

[Spring Security 5.8](https://docs.spring.io/spring-security/reference/5.8/migration/servlet/session-management.html#requestcache-query-optimization)   
[RequestCache](https://docs.spring.io/spring-security/reference/5.8/servlet/architecture.html#requestcache)


## **WebMvcTest 코드 작성**
```java
@WebMvcTest
@Import(WebSecurityConfig.class)
public class WebSecurityConfigTest {

    @Autowired
    private MockMvc mockMvc;
```
`@WebMvcTest`   
Spring MVC 관련 컴포넌트(컨트롤러, 필터 등)만 로드하여 빠른 테스트를 가능하게 한다. 그러나 기본적으로는 보안 설정을 포함하지 않는다.

`@Import`   
WebSecurityConfig 클래스의 보안 설정을 테스트에 포함시킨다.

`MockMvc`   
시뮬레이션할 Mock 객체

`@Nested`   
테스트를 그룹화하고 계층구조로 보기 위해 사용했다.

`@WithMockUser`     
가상의 인증 사용자를 설정

### **Unauthenticated Page Test**
```java
@Nested
@DisplayName("공개된 엔드포인트 테스트")
class PublicEndpoints {

    @Test
    @DisplayName("GET /home은 인증 없이 접근 가능해야 함")
    void testHomePageAccessibleWithoutAuth() throws Exception {
        mockMvc.perform(get("/home"))
                .andExpect(status().isOk())
                .andExpect(view().name("home"));
    }

    @Test
    @DisplayName("GET /은 인증 없이 접근 가능해야 함")
    void testRootAccessibleWithoutAuth() throws Exception {
        mockMvc.perform(get("/"))
                .andExpect(status().isOk())
                .andExpect(view().name("home"));
    }

    @Test
    @DisplayName("GET /login은 인증 없이 접근 가능해야 함")
    void testLoginPageAccessibleWithoutAuth() throws Exception {
        mockMvc.perform(get("/login"))
                .andExpect(status().isOk())
                .andExpect(view().name("login"));
    }
}
```

### **Authenticated Page Test**

```java
@Nested
@DisplayName("보호된 엔드포인트 테스트")
class ProtectedEndpoints {

    @Test
    @DisplayName("GET /hello는 인증이 필요하며, 인증되지 않은 사용자는 로그인 페이지로 리다이렉트되어야 함")
    void testHelloPageRequiresAuth() throws Exception {
        mockMvc.perform(get("/hello"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrlPattern("**/login"));
    }

    @Test
    @WithMockUser(username = "user", roles = {"USER"})
    @DisplayName("GET /hello는 인증된 사용자에게 접근 가능해야 함")
    void testHelloPageAccessibleWithAuth() throws Exception {
        mockMvc.perform(get("/hello"))
                .andExpect(status().isOk())
                .andExpect(view().name("hello"));
    }
}
```

### **Login Test**

```java
@Nested
@DisplayName("로그인 테스트")
class LoginTests {

    @Test
    @DisplayName("올바른 자격 증명으로 로그인 시도 시, 성공적으로 인증되고 /으로 리다이렉트되어야 함")
    void testSuccessfulLogin() throws Exception {
        mockMvc.perform(formLogin("/login")
                        .user("user")
                        .password("password"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/"));
    }

    @Test
    @DisplayName("잘못된 자격 증명으로 로그인 시도 시, 로그인 페이지로 리다이렉트되고 에러가 표시되어야 함")
    void testFailedLogin() throws Exception {
        mockMvc.perform(formLogin("/login")
                        .user("user")
                        .password("wrongpassword"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/login?error"));
    }

    @Test
    @DisplayName("로그인 시 CSRF 토큰이 필요함")
    void testLoginRequiresCsrf() throws Exception {
        mockMvc.perform(formLogin("/login")
                        .user("user")
                        .password("password"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/"));
    }
}
```

### **Logout Test**

```java
@Nested
@DisplayName("로그아웃 테스트")
class LogoutTests {

    @Test
    @WithMockUser(username = "user", roles = {"USER"})
    @DisplayName("로그아웃 시도 시, 세션이 무효화되고 /login?logout으로 리다이렉트되어야 함")
    void testLogout() throws Exception {
        mockMvc.perform(logout("/logout"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/login?logout"));
    }

    @Test
    @DisplayName("로그아웃은 인증되지 않은 사용자도 시도할 수 있으며, /login?logout으로 리다이렉트되어야 함")
    void testLogoutByUnauthenticatedUser() throws Exception {
        mockMvc.perform(logout("/logout"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/login?logout"));
    }
}
```

## **저장소**
[깃허브](https://github.com/YuuuuuuYu/spring-security-example)