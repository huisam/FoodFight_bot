# -*- coding: utf-8 -*-
import json
import csv
import re
import urllib.request
import time
import random

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template
from slacker import Slacker
from threading import Thread
import multiprocessing as mp

app = Flask(__name__)

slack_token = "xoxb-505014660117-507419645299-7ZgXFi1QWfQAAyQ2pDPSKMQq"
slack_client_id = "505014660117.507523199394"
slack_client_secret = "1f7b3a351ceeab9ce32d46c841358eb4"
slack_verification = "IamWoSTzSfYxoPC6LJmrPDLM"
sc = SlackClient(slack_token)

seoul_region = {'wrong': 'wrong', '강남': '09680660', '강동': '09740110', '강북': '09305101', '강서': '09500603', '관악': '09620585', '광진': '09215104',
          '구로': '09530103', '금천': '09545101', '노원': '09350595', '동대문': '09230600', '동작': '09590510', '마포': '09440102',
          '서대문': '09410690', '서초': '09650109', '양천': '09470510', '영등포': '09560550', '용산': '09170104', '종로': '09110146',
                '은평': '09380551', '강릉': '01150615', '고성': '01820250', '동해': '01170113', '삼척': '01230350', '속초': '01210106',
            '양구': '01800310', '가평': '02820250', '과천': '02290103', '광명': '02210107', '광주': '02610101', '구리': '02310101',
                '군포': '02410620', '김포': '02570105'}

flag = {'시작': False, '음식': False, '날씨': False, '대화': False}
channel_name = ['#slackbot-project', '#foodfight_bot_test']
selenium_flag = False

def slack_notify(text=None, channel=channel_name[1], username='FoodFightbot', attachments=None):
    token = 'xoxb-505014660117-507419645299-7ZgXFi1QWfQAAyQ2pDPSKMQq' #토근값은 공개저장소에 공개되지 않도록 주의
    slack = Slacker(token)
    slack.chat.post_message(text=text, channel=channel, username=username, attachments=attachments, as_user=True)


def make_attachment(fallback=None, pretext=None, title=None, title_link=None, text=None, image_url=None):
    attachments = [{
                "fallback": fallback,      # 메세지 알림시 축약형으로 표시
                "color": "#14f5de",        # 옆에 바형 색
                "pretext": pretext,        # '바'가 시작하기 전에 쓰일 문장
                "title": title,            # 진하게 표시되는 문구
                "title_link": title_link,  # 타이틀 누르면 이동
                "text": text,              # 들어갈텍스트
                "image_url": image_url     # 이미지 url연결
            }]
    return attachments


def flag_false():
    for title in flag.keys():
        if not title == '시작':
            flag[title] = False


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


def _info_reader(text):
    text_s = text.split(" ")[1]
    if text_s.isalpha():
        info_s = []
        with open(file="food.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=',')
            local_ = "서울특별시 " + text.split(" ")[1]
            print(str(reader))
            for row in reader:
                if row[6].startswith(local_):
                    try:
                        info = {
                            'name': row[3],
                            'x_': row[4],
                            'y_': row[5],
                            'address': row[6],
                            'ph': row[7]

                        }
                    except:
                        pass
                    info_s.append(info)
        result = []
        str_ = ""

        for j in range(0, 9):
            str_ = "┌----------------------------------------------------------------------┐\n" + ":arrow_forward: 상호명 : " + \
                   info_s[j]["name"] + "\n" + ":arrow_forward: 위치 : " + info_s[j][
                       "address"] + "\n" + ":arrow_forward: P.H : " + info_s[j][
                       "ph"] + "\n" + ":arrow_forward: 지도 : " + selenium_reader(text.split(" ")[1] + " " + info_s[j][
                "name"]) + "\n" + "└----------------------------------------------------------------------┘\n"
            if j==0 :
                attach = make_attachment(fallback="~.~", pretext="★" + text.split(" ")[1] + " 안심먹거리 업소" + "★",
                                         text=str_,title=text + " 검색 결과 입니다")
                slack_notify(attachments=attach)

            else:
                attach = make_attachment(fallback="~.~",text=str_,)
                slack_notify(attachments=attach)
        result = u''.join(str_)

        return result


def select_food(text):
    _info_reader(text)
    flag_false()
    attach = make_attachment(fallback="처음 단계로 돌아가요", pretext="We're going to main event",
                             text="원하시는 서비스를 말씀해주세요\n① 음식\n② 날씨\n③ 나랑 대화"
                             , title="다시 골라주세요!!")
    slack_notify(attachments=attach)


def detect_region(text):
    if '강남' in text:
        region = '강남'
    elif '강동' in text:
        region = '강동'
    elif '강북' in text:
        region = '강북'
    elif '강서' in text:
        region = '강서'
    elif '관악' in text:
        region = '관악'
    elif '광진' in text:
        region = '광진'
    elif '구로' in text:
        region = '구로'
    elif '노원' in text:
        region = '노원'
    elif '동대문' in text:
        region = '동대문'
    elif '동작' in text:
        region = '동작'
    elif '마포' in text:
        region = '마포'
    elif '서대문' in text:
        region = '서대문'
    elif '서초' in text:
        region = '서초'
    elif '양천' in text or '목동' in text:
        region = '양천'
    elif '영등포' in text:
        region = '영등포'
    elif '용산' in text:
        region = '용산'
    elif '종로' in text:
        region = '종로'
    elif '은평' in text:
        region = '은평'
    elif '강릉' in text:
        region = '강릉'
    elif '고성' in text:
        region = '고성'
    elif '동해' in text:
        region = '동해'
    elif '삼척' in text:
        region = '삼척'
    elif '속초' in text:
        region = '속초'
    elif '양구' in text:
        region = '양구'
    elif '가평' in text:
        region = '가평'
    elif '과천' in text:
        region = '과천'
    elif '광명' in text:
        region = '광명'
    elif '광주' in text:
        region = '광주'
    elif '구리' in text:
        region = '구리'
    elif '군포' in text:
        region = '군포'
    elif '김포' in text:
        region = '김포'
    else:
        region = 'wrong'
    return seoul_region[region]


def select_weather(text):
    sign = {'degree': '℃', 'percent': '%', 'time': '시'}
    region = detect_region(text)
    if region != 'wrong':
        url = "https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=" + region
        response = urllib.request.urlopen(url)
        soup = BeautifulSoup(response, "html.parser")
        now_weather = str(soup.find("div", class_="fl"))
        now = now_weather.strip()
        area = str(soup.find("h4", class_="first").get_text())
        dusts = str(soup.find("div", class_="w_now2"))
        dust = re.findall("(.{2})</em>", dusts)[0]

        degree = re.findall("\s(-*\d+)<span>", now)[0]
        raining = re.findall("<strong>(\d+)</strong>", now)[0]
        time = re.findall("<span>(\d+)</span>", now)[0]

        keyword = '┌─────────────┐\n' + '│ ' + area + '\t\t│\n' + '│ 시간 : ' + time + sign['time'] + '  \t\t\t\t│' + \
                  '\n│ 기온 : ' + degree + sign['degree'] + '\t\t\t\t\t│\n│ 강수확률 : ' + raining + sign['percent'] + \
                  '     \t\t│' + '\n│ ' + '미세먼지 : ' + dust + '   \t\t│' '\n└─────────────┘' + '\n□ 더 많은 정보를 원하신다면? □\n' + url
        attach = make_attachment(fallback="날씨궁금궁금궁금", pretext="Here is your area weather", text=keyword
                                 , title="■ 당신의 기상정보 나왔습니다 ■", image_url="https://ssl.pstatic.net/static/weather/images/w_icon/w_t01.gif")
        slack_notify(attachments=attach)
        flag_false()
        attach = make_attachment(fallback="처음 단계로 돌아가요", pretext="We're going to main event",
                                 text="원하시는 서비스를 말씀해주세요\n① 음식\n② 날씨\n③ 나랑 대화"
                                 , title="다시 골라주세요!!")
        slack_notify(attachments=attach)

    else:
        attach = make_attachment(fallback="날씨 단계로 돌아가요", pretext="We're going to weather event",
                                 text="날씨 지역이 어떻게 되시나요?"
                                 , title="다시 입력해 주세요!!")
        slack_notify(attachments=attach)


def conversation_with_bot(text):
    if '그만' in text:
        flag['대화'] = False
        attach = make_attachment(fallback="안녕~~", pretext="돌아간다아아~", text="즐거웠어\n① 음식\n② 날씨\n③ 나랑 대화"
                                 , title="ㅜ.ㅜ")
        slack_notify(attachments=attach)
    else:
        idx = random.randrange(0,7)
        text = ["나는 서울을 꿰고 있는 푸프야!!", "에이 나 너 싫어졌어", "흥칫뿡!!!", "아몬드가 죽으면?\n다이아~몬드~~~",
            "★ssafy 만세★", "1010101010100000011010"]
        attach = make_attachment(fallback="헤헤 *-*", pretext="푸드파이터의 답변 :", text='=======================\n돌아가고 싶으면 [그만]을 외쳐줘'
                                 , title=text[idx])
        slack_notify(attachments=attach)


def conversation_main(text):
    if flag['대화']:
        conversation_with_bot(text)
    else:
        flag['대화'] = True
        attach = make_attachment(fallback="나랑 놀자아아~!", pretext="★☆★☆★☆★☆★", text="나의 어떤점이 궁금해? *^-^*"
                                 , title="롸잇~나우★ 핫해~하태~hot해~")
        slack_notify(attachments=attach)


def food_main(text):
    if flag['음식']:
        select_food(text)
    else:
        flag['음식'] = True
        attach = make_attachment(fallback="음식을 골라골라", pretext="Where is your area?", text="서울안전먹거리 - 살고계신 지역(구)를 입력해주세요"
                                 , title="먹고 싶은 지역이 어떻게 되시나요?")
        slack_notify(attachments=attach)


def weather_main(text):
    if flag['날씨']:
        select_weather(text)
    else:
        flag['날씨'] = True
        attach = make_attachment(fallback="날씨를 골라골라", pretext="Where is your area?", text="▶○○(구/시)로 말씀해주세요!!◀\n\tEx) 강남구\n\t\t  종로구\n\t\t  강남"
                                 , title="날씨 지역이 어떻게 되시나요?")
        slack_notify(attachments=attach)


def start_chat_bot(text):
    flag['시작'] = True
    attach = make_attachment(fallback="어서오세요!!", pretext="★Welcome to FoodFightBot★", text="① 음식\n② 날씨\n③ 나랑 대화"
                             ,title="무엇을 알려드릴까요?")
    slack_notify(attachments=attach)


# 텍스트를 통한 응답 함수
def _crawl_naver_keywords(text):
    # 여기에 함수를 구현해봅시다.
    if "시작" in text and not flag['시작']:
        start_chat_bot(text)
        return
    elif "음식" in text or "1" in text and flag['음식']:
        food_main(text)
        return
    elif "날씨" in text or "2" in text or flag['날씨']:
        weather_main(text)
        return
    elif "대화" in text or "3" in text and flag['대화']:
        conversation_main(text)
        return
    else:
        flag_false()
        attach = make_attachment(fallback="처음 단계로 돌아가요", pretext="We're going to main event", text="원하시는 서비스를 말씀해주세요\n① 음식\n② 날씨\n③ 나랑 대화"
                             ,title="다시 골라주세요!!")
        slack_notify(attachments=attach)
        return


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    event_queue.put(slack_event)
    return make_response("App mention message has been sent", 200, )


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event and selenium_flag == False:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


def processing_event(queue):
   while True:
       # 큐가 비어있지 않은 경우 로직 실행
       if not queue.empty():
           slack_event = queue.get()

           # Your Processing Code Block gose to here
           channel = slack_event["event"]["channel"]
           text = slack_event["event"]["text"]

           # 챗봇 크롤링 프로세스 로직 함수
           keywords = _crawl_naver_keywords(text)


if __name__ == '__main__':
    event_queue = mp.Queue()

    p = Thread(target=processing_event, args=(event_queue,))
    p.start()
    print("subprocess started")

    app.run('127.0.0.1', port=8080)
    p.join()