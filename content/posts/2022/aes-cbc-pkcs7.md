---
title: AES/CBC/PKCS7
author: nakji
date: 2022-07-12 14:23:00 +0900
tags: [Theory, Security, encrypt, aes, cbc, pkcs7]
showToc: true
TocOpen: true
comments: true
disableHLJS: false # to disable highlightjs
disableShare: false
disableHLJS: false
hideSummary: false
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
UseHugoToc: true
---
용어 자체가 거창해보이지만 하나씩 해석해보면

**AES** *대칭키 암호화 방식* 중 하나이고  
**CBC**는 블록 단위로 암호화를 하는 *AES 방식의 운영모드* 중 하나이다.    
**PKCS7**은 AES128 방식을 쓴다고 하면, 128비트보다 *작은 블록이 나오면 뒤에 값을 붙여주는* '**패딩**'의 한 방식이다.

크게 암호화 방식은 대칭키, 비대칭키 방식이 있다.    
**대칭키**는 암호화/복호화에 쓰이는 키가 같아서 *속도가 빠르지만* 해당 키값이 노출되면 문제가 생기고 관리가 쉽지 않다.

위에서 말한 **AES**는 DES방식의 결함이 발견되어 채택된 방식으로 128/192/256비트의 *고정 블록 단위*로 암호화를 수행한다.  
특히 블록 암호화 방식은 *평문의 길이와 상관없이 고정된 길이*가 나오게 된다.

평문을 패딩을 통해 블록 크기의 배수로 만들고나면 일정한 크기의 블록으로 나누어서 암호화를 하고 연결하게 된다.   
ex) 12345678abcdefgh -> 1234, 5678, abcd, efgh  
=> AKFM, IJRM, CSjs, Q23I -> AKFMIJRMCSjsQ23I

여기에 사용되는 운용 방식으로 **CBC** 방식이 있는데 *키가 고정되어 있는 경우* 암호화한 결과가 동일하게 나올 수 있으므로 이를 해결하고자 나온 방식이다.

이는 첫 번째 블록(1234)을 **Iv값(첫 번째 블록을 암호화하는 키값)**으로 암호화를 하여 AKFM 라는 값을 얻었으면 이 AKFM값으로 다음 블록을 암호화시킨다.

따라서 위의 예시로 들었던 평문을 **'a1b2'**라는 값으로 암호화하여 나온 값이라면 CBC 방식을 사용했을 때 첫 번째 블록의 암호화값이 AKFM이 나올 수 있지만 그 다음 블록의 값부터는 달라지게 된다.

출처    
[Tistory 1](https://liveyourit.tistory.com/183)     
[Tistory 2](https://yjshin.tistory.com/entry/%EC%95%94%ED%98%B8%ED%95%99-%ED%98%84%EB%8C%80-%EB%8C%80%EC%B9%AD%ED%82%A4-%EC%95%94%ED%98%B8%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%95%94%ED%98%B8%ED%99%94-%EA%B8%B0%EB%B2%95-ECB-CBC-CFB-OFB-CTR-%EB%AA%A8%EB%93%9C)  
[Secmem](https://www.secmem.org/blog/2019/02/06/block-cipher/)  
[Velog](https://velog.io/@sgh002400/AESCBCPKCS7Padding-%EC%95%94%EB%B3%B5%ED%98%B8%ED%99%94)