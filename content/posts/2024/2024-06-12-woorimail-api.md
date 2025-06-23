---
title: 우리메일 API를 이용한 배치 스크립트
author: nakji
date: 2024-06-12 14:44:00 +0900
tags: [Email, WooriMail, Shell]
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
```
#!/bin/bash

######### NOTICE ##############
#	 Itsm 요청이 왔을 때
#	메일 발송되는 것이 목적이라서
#	 아래 소스는 ChatGPT로
#	최소한의 로직만 구현했습니다
###############################

######## MAIL API ############
#    우리메일(WOORIMAIL)
#  https://woorimail.com
#						
#  월 1만건 무료 발송 가능합니다
# 	 메일 1만건 모두 소진 시
# 	당월 메일 발송이 중지됩니다
##############################

###### TIME SETTING ###########
# 	 현재 9시 ~ 18시까지만
#	 동작하도록 세팅되어있으니
#	수정이 필요하면 아래 함수에서
#	  시간 수정 부탁드립니다
#  check_working_hours()
###############################

##### RECEIVER INFO ###########
# 	 메일 발신자 정보 수정은
# 	60번 줄 영역에 있는 값을
# 	  수정해주시면 됩니다
###############################

# Function to make API call and check response
check_response() {
  # API details
  METHOD="POST"
  CONTENT_TYPE="application/x-www-form-urlencoded"
  ITSM_CHECK_URL="" # ITSM 접수대기 건수 URL
  ITSM_LIST_URL="" # ITSM 접수대기 리스트 URL
  BODY="id=1520" # 접수대기(1520), 처리중(1526)

  # ITSM 처리중
  #ITSM_LIST_URL=""
  #BODY="id=1526"
  
  # 고정값
  MAIL_URL="https://woorimail.com/"
  TYPE="api"
  MID="auth_woorimail"
  ACT="dispWwapimanagerMailApi"
  DOMAIN="" # 지정한 도메인 URL
  AUTHKEY="" # 키값
  
  ##################################################
  # 아래처럼 세팅했을 경우 메일은 다음과 같이 발송됩니다
  #
  # 발신자: YuY<wms_nick@mx.woorimail.com>
  # 회신할 경우, 받는사람: ID@이메일주소
  ##################################################
  WMS_NICK="wms_nick"               # 보낸사람 계정
  SENDER_EMAIL=""                   # 회신할 사람 이메일
  SENDER_NICKNAME="YuY"             # 회신할 사람 닉네임
  RECEIVER_NICKNAME=""              # 받는 사람(나) 닉네임
  RECEIVER_EMAIL=$RECEIVER_EMAIL    # 받는 사람(나) 이메일
  
  # Add cookies to the request
  COOKIE="JSESSIONID=$JSESSIONID"   # ITSM JSessionID 값

  # Make the API call and print the response
  RESPONSE=$(curl -s -X $METHOD \
                    -H "Content-Type: $CONTENT_TYPE" \
                    -H "Cookie: $COOKIE" \
                    -d "$BODY" \
                    $ITSM_CHECK_URL)

  # Extract result value from RESPONSE message
  RESULT_ITSM_READY_CNT=$(echo "$RESPONSE" | grep -oP 'result: \(\K[0-9]+')

  # Check if RESULT is greater than 0 and show dialog
	if validate_email "$RECEIVER_EMAIL"; then
		if [ "$RESULT_ITSM_READY_CNT" -gt 0 ]; then 
		
			RESPONSE=$(curl -s -X $METHOD \
                                            -H "Content-Type: $CONTENT_TYPE" \
                                            -H "Cookie: $COOKIE" \
                                            -d "$BODY" \
                                            $ITSM_LIST_URL)
						
			RESULT_ITSM_READY_LIST=$(echo "$RESPONSE" | sed -n '/<table width="100%"/,/<\/table>/p' | sed -n '1,/<\/table>/p' | grep -o '<td[^>]*>[^<]*</td>' | sed -E 's/<\/?td[^>]*>//g')
			RESULT_ITSM_ALL_HTML=$(echo "$RESPONSE" | sed ':a;N;$!ba;s/\n/ /g' | grep -oP '<table width="100%".*?</table>')
						
			# Convert the multiline string to an array
			IFS=$'\n' read -r -d '' -a TD_VALUES_ARRAY <<< "$RESULT_ITSM_READY_LIST"
			MAIL_TITLE="ITSM "
			
			# Process the array in chunks of 7
			num_values=${#TD_VALUES_ARRAY[@]}
			for ((i = 0; i < num_values; i += 7)); do
			  MAIL_TITLE="$MAIL_TITLE ${TD_VALUES_ARRAY[i]} "
			done
			
			MAIL_TITLE=$(url_encode "$MAIL_TITLE")
			MAIL_CONTENT=$(url_encode "ITSM 대기건수: $RESULT_ITSM_READY_CNT 건 $RESULT_ITSM_ALL_HTML")
			MAIL_BODY="authkey=$AUTHKEY&domain=$DOMAIN&type=$TYPE&mid=$MID&act=$ACT&callback=&title=$MAIL_TITLE&content=$MAIL_CONTENT&wms_domain=woorimail.com&wms_nick=$WMS_NICK&sender_email=$SENDER_EMAIL&sender_nickname=$SENDER_NICKNAME&receiver_nickname=$RECEIVER_NICKNAME&receiver_email=$RECEIVER_EMAIL&member_regdate=20240604170101"
			
			RESPONSE=$(curl -s -X $METHOD \
                                            -H "Content-Type: $CONTENT_TYPE" \
                                            -d "$MAIL_BODY" \
                                            $MAIL_URL)
			echo "Ready Itsm: $RESULT_ITSM_READY_CNT, $RESPONSE"
		else
			echo "Empty Itsm."
		fi
	else
		echo "Invalid email format. Please provide a valid email address."
	fi
}

# Function to check if current time is within working hours
check_working_hours() {
  current_hour=$(date +%H)
  if [ "$current_hour" -ge 9 ] && [ "$current_hour" -lt 18 ]; then
    return 0 # Within working hours
  else
    return 1 # Outside working hours
  fi
}

# Function to validate email format
validate_email() {
  # Regular expression for email validation
  regex='^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
  
  if [[ $1 =~ $regex ]]; then
    return 0 # Valid email format
  else
    return 1 # Invalid email format
  fi
}

# Function to URL encode a string
url_encode() {
  local string="${1}"
  local encoded=""

  # Convert the string to hex representation
  hex_string=$(echo -n "$string" | od -An -tx1 | tr ' ' '\n' | grep -v '^$')

  # Iterate over each character in the hex string
  for hex_char in $hex_string; do
    encoded+="%$hex_char"
  done

  echo "$encoded"
}

INTRODUCTION="
################################################
###### ITSM 로그인 후
###### 쿠키에 등록된 JSESSIONID 값을 입력해주세요
################################################

################################################
# 입력 파라미터, 몇분마다 이메일로 발송할지 세팅
# 1: 시간, 분(minute)
# 2: 이메일 주소
#
# ex) ./checkItsm.sh 5 이메일주소
# -> 5분마다 접수대기 중인 itsm을 체크하여
# -> 1건 이상 있을 경우 입력한 이메일로 발송
#
# Itsm이 장시간으로 접수대기 상태인 경우가 많을수록
# 시간을 길게 세팅하는게 좋습니다
# 권장 시간(분) 5 ~ 20
################################################

값을 제대로 입력하면 아래와 같은 형식의 문구가 나옵니다
- 접수대기 건수가 없는 경우
> Empty Itsm.

- 접수대기 건수가 있는 경우, 메일 발송
> Ready Itsm: 1, result: ~~, error_msg: ~~ ...

JSESSIONID: "

# Prompt user to input JSESSIONID
read -p "$INTRODUCTION" JSESSIONID

# Check if the second argument is provided
if [ -z "$2" ]; then
  echo "Please provide a RECEIVER_EMAIL as the second argument."
  exit 1
else
  RECEIVER_EMAIL="$2"
fi

# Check if argument is provided for interval, default is set to 5 minutes
interval=${1:-5}

# Loop indefinitely and check response every $interval minutes
while true; do
	# Check if current time is within working hours
  if ! check_working_hours; then
    echo "Outside working hours. Exiting..."
    exit 0
  fi
  
  check_response
  sleep "$interval"m
done
```