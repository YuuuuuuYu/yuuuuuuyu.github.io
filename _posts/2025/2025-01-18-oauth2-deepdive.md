---
title: OAuth2 Deepdive
author: nakji
date: 2025-01-18 11:48:00 +0900
categories: [Theory, Deepdive]
tags: [Security, oauth2, authentication, authorization]
pin: false
img_path: ''
---
🔔 **Oauth2 적용 전**   
🔔 **Oauth2 실습**   

## 개요
최근 개인 프로젝트에서 네이버 로그인을 위해 필요한 부분을 설정하고 로직을 구현했다. 개발 가이드에 맞게 각 단계별로 진행을 했으나...

아무리 봐도 ***과정 하나 하나를 내 손으로 직접 구현하는게 맞는건가?*** 라는 의문을 시작으로 좀 더 효율적으로 구현하는 방법을 찾아봤고, 그렇게 `Oauth 2.0`으로 로그인하는 방식을 찾게 되었다.

## Oauth2 적용 전
코드 스타일을 떠나서 지금 와서 보니 마치 `Oauth 1.0`처럼 구현을 하고 있었다. 나 또한, 각 플로우마다 하드 코딩은 줄이고 변수나 함수를 재활용하기 위해, 보안 요소를 생각하면서 구현했었다.

서드 파티 관련 API를 호출할 때, 응답 값을 Json으로 가져오기 위해 `JsonNode`를 많이 사용했는데 동일하게 적용하려고 보니 소스가 너무 길어진 것 같다.

<details>
<summary>소스 보기/닫기</summary>

```
private final NaverApiService naverApiService;
private final SnsInfoService snsInfoService;
private final UserService userService;

public String getNaverOauth2LoginUrl(HttpServletRequest request) {
    String authorizeUrl = BASE_URL+"/authorize";
    String callbackUrl = getServiceUrl()+"/login/naver/callback";
    String state = NakjiUtil.generateTokenState();
    request.getSession().setAttribute("state", state);

    return UriComponentsBuilder
            .fromHttpUrl(authorizeUrl)
            .queryParam("response_type", "code")
            .queryParam("client_id", secrets.naver().naverId())
            .queryParam("redirect_uri", callbackUrl)
            .queryParam("state", state)
            .toUriString();
}

public String processNaverLogin(LoginProfile profile, Oauth2AccessToken tokenInfo) {
    SnsInfo checkSnsInfo = snsInfoService.getOrCreateUser(profile, tokenInfo);
    Optional<User> user = userService.getUserByUserId(checkSnsInfo.getSnsId());
    if (user.isPresent()) {
        // Update user info

    } else {
        // Create user
    }
    return "redirect:/";
}

public String processNaverLoginCallback(String state, String code, HttpSession session) {
    Oauth2AccessToken token = getToken(state, code, session);
    if (token == null) {
        throw new BadRequestException(ErrorCode.INVALID_PARAMETER);
    }

    try (Response response = naverApiService.naverProfileConnection(token.tokenType(), token.accessToken())) {
        if (response.status() == 200) {
            JsonNode resultJson = NakjiUtil.readBody(response.body().asInputStream());
            if ("00".equals(resultJson.get("resultcode")) && "success".equals(resultJson.get("message"))) {
                JsonNode profileInfo = resultJson.get("response");
                LoginProfile profile = new LoginProfile("naver",
                        Optional.ofNullable(profileInfo.get("id")).map(JsonNode::asText).orElse(""),
                        Optional.ofNullable(profileInfo.get("nickname")).map(JsonNode::asText).orElse(""),
                        Optional.ofNullable(profileInfo.get("gender")).map(JsonNode::asText).orElse(""),
                        Optional.ofNullable(profileInfo.get("age")).map(JsonNode::asText).orElse("")
                );

                return processNaverLogin(profile, token);
            } else {
                throw new Exception();
            }
        } else {
            log.info("NaverLoginService.getNaverProfileUrl Request Status: {}, Body: {}", response.status(), response.body().toString());
            //throw new BadRequestException("Bad request with status: " + response.status());
        }
    } catch (Exception e) {
        log.error("NaverLoginService.getNaverProfileUrl Error: ", e);
    }

    return "";
}

public Oauth2AccessToken getToken(String state, String code, HttpSession session) {
    try (Response response = getGenerateToken(state, code, session)) {
        if (response.status() == 200) {
            JsonNode resultJson = NakjiUtil.readBody(response.body().asInputStream());
            Oauth2AccessToken resultToken = new Oauth2AccessToken(
                    Optional.ofNullable(resultJson.get("access_token")).map(JsonNode::asText).orElse(""),
                    Optional.ofNullable(resultJson.get("refresh_token")).map(JsonNode::asText).orElse(""),
                    Optional.ofNullable(resultJson.get("token_type")).map(JsonNode::asText).orElse(""),
                    Optional.ofNullable(resultJson.get("expires_in")).map(JsonNode::asInt).orElse(0),
                    Optional.ofNullable(resultJson.get("error")).map(JsonNode::asText).orElse(""),
                    Optional.ofNullable(resultJson.get("error_description")).map(JsonNode::asText).orElse("")
            );

            if ("invalid_request".equals(resultToken.errorCode())) {
                throw new BadRequestException(ErrorCode.INVALID_PARAMETER);
            } else if ("unauthorized_client".equals(resultToken.errorCode())) {
                throw new UnauthorizedException(ErrorCode.INVALID_AUTH_CODE);
            }

            return resultToken;
        } else {
            log.info("NaverLoginService.getToken Request Status: {}, Body: {}", response.status(), response.body().toString());
            //throw new BadRequestException("Bad request with status: " + response.status());
        }
    } catch (Exception e) {
        log.error("NaverLoginService.getToken Error: ", e);
    }

    return null;
}

private Response getGenerateToken(String state, String code, HttpSession session) {
    String storedState = (String)session.getAttribute("state");
    if (!state.equals(storedState)) {
        throw new UnauthorizedException(ErrorCode.INVALID_AUTH_PATH);
    }

    return Feign.builder()
            .encoder(new GsonEncoder())
            .decoder(new GsonDecoder())
            .target(NaverGenerateTokenClient.class, BASE_URL)
            .generateToken(secrets.naver().naverId(), secrets.naver().naverKey(), state, code);
}
```

</details>

## Oauth2 적용 후
gpt와 일부 블로그를 찾아보면서 내 방식대로 적용해봤다. 우선 로그인은 잘 되고, 초기 세팅만 해두면 그 이후에는 소스를 재활용하거나 조금만 더 추가하는 것으로 해결될 것 같다.

다음에는 페이지마다 역할 부여하는 것과 jwt을 이용한 로그인을 추가할 예정이다.

### security.yml
```
spring:
  security:
    oauth2:
      client:
        registration:
          naver:
            client-id: ${NAVER_CLIENT_ID}
            client-secret: ${NAVER_CLIENT_SECRET}
            authorization-grant-type: authorization_code
            redirect-uri: ${SERVICE_URL}${NAVER_REDIRECT_URI}
            scope: name, nickname, email, gender, birthyear, profile_image
        provider:
          naver:
            authorization-uri: https://nid.naver.com/oauth2.0/authorize
            token-uri: https://nid.naver.com/oauth2.0/token
            user-info-uri: https://openapi.naver.com/v1/nid/me
            user-name-attribute: response

```

### SecurityConfig
```
@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {
    private final CustomOAuth2UserService customOAuth2UserService;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
                .csrf(csrf -> csrf.disable())
                .authorizeHttpRequests(authorize -> authorize
                        ...
                )
                .oauth2Login(oauth2 -> oauth2
                        .loginPage("/login")
                        .defaultSuccessUrl("/")
                        .failureUrl("/login?error")
                        .userInfoEndpoint(userInfo -> userInfo
                                .userService(customOAuth2UserService)
                        )
                )
                .logout(logout -> logout
                        .logoutSuccessUrl("/")
                        .invalidateHttpSession(true)
                        .deleteCookies("JSESSIONID")
                )
                .build();
    }
}
```

### OAuthAttributes
```
@Builder
public record OAuthAttributes(Map<String, Object> attributes, String nameAttributeKey, User user) {
    public static OAuthAttributes of(String registrationId, String userNameAttributeName, Map<String, Object> attributes) {
        if ("naver".equals(registrationId)) {
            return ofNaver(userNameAttributeName, attributes);
        } else {
            return null;
        }
    }

    private static OAuthAttributes ofNaver(String userNameAttributeName, Map<String, Object> attributes) {
        Map<String, Object> response = (Map<String, Object>) attributes.get("response");

        return OAuthAttributes.builder()
                .attributes(attributes)
                .nameAttributeKey(userNameAttributeName)
                .user(User.builder()
                        .oauthId((String) response.get("id"))
                        .provider("naver")
                        .name((String) response.get("name"))
                        .nickname((String) response.get("nickname"))
                        .profileImage((String) response.get("profile_image"))
                        .email((String) response.get("email"))
                        .gender((String) response.get("gender"))
                        .birthYear((String) response.get("birthYear"))
                        .role(Role.USER)
                        .build())
                .build();
    }

    public User toEntity() {
        return user;
    }
}
```

### OAuth2UserService
```
@Service
@RequiredArgsConstructor
public class CustomOAuth2UserService implements OAuth2UserService<OAuth2UserRequest, OAuth2User> {
    private final UserRepository userRepository;
    private final HttpSession httpSession;

    @Override
    public OAuth2User loadUser(OAuth2UserRequest userRequest) throws OAuth2AuthenticationException {
        OAuth2UserService<OAuth2UserRequest, OAuth2User> delegate = new DefaultOAuth2UserService();
        OAuth2User oAuth2User = delegate.loadUser(userRequest);
        String registrationId = userRequest.getClientRegistration().getRegistrationId();
        String userNameAttributeName = userRequest.getClientRegistration()
                                        .getProviderDetails()
                                        .getUserInfoEndpoint()
                                        .getUserNameAttributeName();

        OAuthAttributes attributes = OAuthAttributes.of(registrationId, userNameAttributeName, oAuth2User.getAttributes());
        User user = saveOrUpdate(attributes);
        httpSession.setAttribute("user", new SessionUser(user));

        return new DefaultOAuth2User(
                Collections.singleton(new SimpleGrantedAuthority(user.getRoleKey())),
                attributes.getAttributes(),
                attributes.getNameAttributeKey());
    }

    private User saveOrUpdate(OAuthAttributes attributes) {
        User userInfo = attributes.getUser();
        User target = userRepository.findByOauthId(userInfo.getOauthId())
                .map(entity -> entity.update(userInfo.getNickname(), userInfo.getProfileImage(), userInfo.getEmail()))
                .orElse(attributes.toEntity());

        return userRepository.save(target);
    }
}
```

## 후기
여담이지만 키값을 관리할 때, 해당 설정 파일을 저장소에는 커밋하지 않았다. 다른 PC에서 접속할 때는 개인 클라우드에서 키값이 있는 파일을 불러와서 사용했는데, 이번에 oauth를 경험하면서 점점 불편해질 수 있을 것 같다.

그래서 dotenv를 사용하고 기존 환경설정 값들은 env 파일에서 가져오는 방식으로 수정했다.      
큰 차이는 없을 수 있지만, 내가 환경설정할 때 어떤 구조로 설정했는지는 볼 수 있게 된 것이 개선점이다.

## 참고 자료
[Spring io](https://docs.spring.io/spring-security/reference/servlet/oauth2/login/core.html)    
[Velog](https://iseunghan.tistory.com/300)  
ChatGPT
