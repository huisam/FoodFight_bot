---
title: 자기 주도 학습
---

# 주제1

<div>

<img width="200" src="http://www.dtoday.co.kr/news/photo/201712/258866_174898_1849.jpg">

##  Design Thinking

</div>

<div>
	
|단계|정의|활용 Tool|
|---|---|---|
|공감|관찰, 인터뷰, 체험으로 문제점을 발견|공감지도, 고객여정맵 만들기|
|문제 정의|문제점에 대해 정의하고 분석하기|페르소나 만들기|
|아이디어 도출|아이디어를 자유롭게 발산하는 과정|마인드맵, 브레인라이팅, SCAMPER|
|프로토타입|아이디어를 구현하는 과정|목업툴(justinmind, balsamiq, adobe)|
|테스트|피드백을 통해 아이디어를 개선|PMI 피드백|

</div>

# 주제2


<div>

# <img width="60" src="https://user-images.githubusercontent.com/30898520/50325037-cd6e5680-0525-11e9-8bbe-ac5014ab9c33.jpg"> ChatBot

##  Flask를 이용한 Slack_ChatBot

</div>

#### FoodFigter_ChatBot은 룰 기반 형식의 챗 봇입니다.    
다음 챗봇은 크게 3가지 제공되는 기능을 이용하실 수 있습니다.  
* 음식
* 날씨
* 대화  

<br/><br/>

## 사용법

### 0. 첫 시작

#### 기본적 사용법으로는 @"봇 이름" (명령) 입니다.
다음은 처음 ChatBot을 호출하여 응답이 시작되는 첫 화면 입니다.

<div>
 <img width="400" height="250" src="https://user-images.githubusercontent.com/30898520/50325130-7321c580-0526-11e9-87e2-d07e65a703fc.PNG">
</div>

   
### 1. 음식

봇을 호출 한 뒤 첫번째로 음식에 대해 명령을 내리는 모습입니다.

지역은 서울을 기준으로 살고있는 지역(구)에 대한 입력을 받습니다.   
그리고 그 지역에 대한 음식점에 대한 정보를 셀레니움을 통해 크롤링하여 읽어 옵니다.

<div>
  <img width="400" src="https://user-images.githubusercontent.com/30898520/50325259-183c9e00-0527-11e9-8a8c-73c3f305f7e9.PNG">
  <img width="400" src="https://user-images.githubusercontent.com/30898520/50325302-63ef4780-0527-11e9-967d-ff18e8276a28.PNG">
</div>

>* 셀레니움을 통한 지도 관련 uri를 가져오는 코드입니다.

    def selenium_reader(address):
    	options = webdriver.ChromeOptions()
    	options.add_argument('headless')
    	options.add_argument('window-size=1920x1080')
    	options.add_argument("--disable-gpu")

    	driver = webdriver.Chrome("C:\\Users\\student\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=options)

    	# url에 접근한다
    	driver.get('https://www.google.com/maps/')
    	print(address)
    	driver.find_element_by_id('searchboxinput').send_keys(address)
    	driver.find_element_by_id("searchboxinput").send_keys(Keys.ENTER)

    	time.sleep(3)

    	print(driver.current_url)
    return driver.current_url
   
<br/><br/>


### 2. 날씨

다음은 날씨에 관련하여 ChatBot에게 오늘 날씨를 물어보는 모습입니다.    
위 음식 질문과 같이 지역(구) 입력을 통하여 날씨 api를 이용해 결과를 받아 볼 수 있습니다. 

<div>
	
  <img width="400" src="https://user-images.githubusercontent.com/30898520/50325591-1c69bb00-0529-11e9-8c26-d0c9524f9374.PNG">
  <img width="400" src="https://user-images.githubusercontent.com/30898520/50325731-dc570800-0529-11e9-8b11-56723bb48124.PNG">
  
</div>
<br/><br/>



### 3. 대화

대화에서는 Bot과 함께 자유롭게 대화를 나눌 수 있습니다.

<div>
   <img width="400" src="https://user-images.githubusercontent.com/30898520/50325789-32c44680-052a-11e9-8185-4be351d84642.PNG">
   <img width="400" src="https://user-images.githubusercontent.com/30898520/50325790-3526a080-052a-11e9-9a15-d43a7652f877.PNG">
	
</div>

