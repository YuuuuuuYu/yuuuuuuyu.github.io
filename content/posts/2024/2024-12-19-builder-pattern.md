---
title: 빌더 패턴 (Builder Pattern)
author: nakji
date: 2024-12-19 13:02:00 +0900
tags: [design pattern, builder]
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
🔔 **빌더 패턴이란?**   
🔔 **기존 생성자 방식과의 차이점**

## **What? Why?**
빌더 패턴(Builder Pattern)은 복잡한 객체를 단계별로 생성할 수 있게 해주는 디자인 패턴이다. 객체의 생성 과정을 추상화하여, 다양한 형태의 객체를 유연하게 생성할 수 있도록 도와준다.

## **기존 생성자 방식과의 비교**
### **기존 생성자 방식**
기존의 생성자 방식은 객체를 생성할 때 필요한 모든 파라미터를 생성자에 전달해야 한다.

```
public class User {
    private Long id;
    private String userId;
    private String username;
    private Set<Role> roles;
    // 기타 필드 및 메서드

    public User(Long id, String userId, String username, Set<Role> roles) {
        this.id = id;
        this.userId = userId;
        this.username = username;
        this.roles = roles;
    }
}
```

### **빌더 패턴 방식**
빌더 패턴을 사용하면 객체의 필드를 단계별로 설정할 수 있으며, 가독성이 높아지고 선택적인 필드를 쉽게 처리할 수 있다.

```
User user = User.builder()
                .userId("uniqueUserId123")
                .username("홍길동")
                .roles(new HashSet<>())
                .build();
```

## **빌더 패턴이 등장하게 된 계기**
기존의 생성자 방식은 매개변수가 많아지면 코드가 복잡해지고 가독성이 떨어지는 단점이 있다. 

특히, 동일한 타입의 여러 파라미터가 있을 경우 실수하기 쉽다. 이러한 문제를 해결하기 위해 빌더 패턴이 등장하게 되었다.

### 장단점 비교
**빌더 패턴의 장점**
1.  **가독성 향상**     
    메서드 체이닝을 통해 어떤 필드에 어떤 값을 설정하는지 명확하게 드러난다.

2.  **유연성**      
    선택적인 필드를 쉽게 설정할 수 있으며, 필드의 순서에 상관없이 값을 지정할 수 있다.

3.  **불변 객체 생성**  
    빌더 패턴을 사용하면 객체를 불변으로 만들기 쉽다.

4.  **복잡한 객체 생성 용이**   
    객체 생성 과정이 복잡한 경우 빌더 패턴이 더욱 효과적이다.

**빌더 패턴의 단점**
1.  **코드량 증가**    
    별도의 빌더 클래스를 작성하거나, Lombok과 같은 라이브러리를 사용하지 않으면 코드가 길어질 수 있다.

2.  **성능 오버헤드**   
    매우 빈번한 객체 생성을 요구하는 경우 빌더 패턴은 약간의 성능 오버헤드를 유발할 수 있다. 하지만 대부분의 경우 이는 큰 문제가 되지 않는다.

**생성자 방식의 장점**
1.  **간단함**     
    단순한 객체를 생성할 때는 생성자 방식이 더 간단하고 직관적이다.

2.  **성능**   
    빌더 패턴에 비해 약간의 성능 이점을 가질 수 있다.

**생성자 방식의 단점**
1.  **가독성 저하**    
    매개변수가 많아지면 생성자의 가독성이 떨어진다.

2.  **유연성 부족**    
    선택적인 필드를 설정하기 어렵고, 필드의 순서에 의존하게 된다.

3.  **유지보수 어려움**    
    필드가 추가되거나 변경될 때마다 생성자도 수정해야 한다.

## **요약**
빌더 패턴은 객체 생성 시 가독성과 유연성을 높이고, 복잡한 객체를 보다 쉽게 생성할 수 있게 해준다. 특히 필드가 많거나 선택적인 필드가 있는 경우 빌더 패턴이 매우 유용하다.

반면, 단순한 객체 생성에는 기존의 생성자 방식이 더 간단할 수 있다. 상황에 맞게 적절한 패턴을 선택하는 것이 중요하다.