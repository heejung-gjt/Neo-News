
import time
import requests
import django
import os
import sys
from bs4 import BeautifulSoup
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/app')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


# datetime -> time 객체로 만들어줌
def convert_datetime_to_timestamp(date_list):
    if date_list[4] == "오전":
        date_list[4] = "AM"
    else:
        date_list[4] = "PM"

    date_string = f'{date_list[0]}-{date_list[1]}-{date_list[2]} {date_list[4]} {date_list[5]}:{date_list[6]}'
    datetime_obj = datetime.strptime(date_string, '%Y-%m-%d %p %I:%M')
    return datetime.timestamp(datetime_obj)

naver_news_code = {
    '100' : [264, 265, 266],
    '101' : [259, 258, 261],
    '102' : [249, 250, 251],
    '103' : [241, 239, 240],
    '104' : [231, 232, 233],
    '105' : [731, 226, 227],
}


def convert_datetime_to_timestamp(date_list):
    if date_list[4] == "오전":
        date_list[4] = "AM"
    else:
        date_list[4] = "PM"

    date_string = f'{date_list[0]}-{date_list[1]}-{date_list[2]} {date_list[4]} {date_list[5]}:{date_list[6]}'
    datetime_obj = datetime.strptime(date_string, '%Y-%m-%d %p %I:%M')
    return datetime.timestamp(datetime_obj)

naver_news_code = {
    '100' : [264, 265, 266],
    '101' : [259, 258, 261],
    '102' : [249, 250, 251],
    '103' : [241, 239, 240],
    '104' : [231, 232, 233],
    '105' : [731, 226, 227],
}


def parse_naver():
    category_list = [key for key in naver_news_code.keys()]
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}
    
    news_info = []
    for naver_category in category_list:
        scraped_date = datetime.today().strftime("%Y%m%d")
        for sub_category in naver_news_code[naver_category]:
            for num in range(1,4):
                time.sleep(1)
                print(f'{naver_category} - {sub_category} - {num} 페이지 스크래핑 시작 -!')
                url = f'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2={sub_category}&sid1={naver_category}&date={scraped_date}&page={num}'
                res = requests.get(url, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')

                headline = soup.select("#main_content > div.list_body.newsflash_body > ul.type06_headline > li")

                news_uls = [headline]  # 총 20개의 기사 스크래핑 가능
                

                for news_ul in news_uls:
                    for news_li in news_ul:
                        try:
                            category_name = soup.select_one("#snb > h2 > a").text
                            press = news_li.select_one("dl > dd > span.writing").text
                            preview_img = news_li.select_one("li > dl > dt.photo > a > img")['src']
                            title = news_li.select_one("dl > dt:nth-child(2) > a").text.strip()
                            ref = news_li.select_one("dl > dt:nth-child(2) > a")['href']
                            
                            # 기사 코드, 상세내용, 날짜 스크래핑
                            article_res = requests.get(ref, headers=headers)
                            article_soup = BeautifulSoup(article_res.text, 'html.parser')
                            kakao_img = article_soup.select_one('#articleBodyContents > span.end_photo_org > img')['src']
                            code = ref.split("aid=")[1]
                            content = article_soup.select_one("#articleBodyContents")  # 태그 타입임, str(content) 해줘야 함
                            date_str = article_soup.select_one("#main_content > div.article_header > div.article_info > div > span.t11").text
                            data = {
                                'category' : category_name,
                                'press' : press,
                                'code' : code,
                                'preview_img' : preview_img,
                                'title' : title,
                                'content': str(content),
                                'date' : date_str,
                                'ref' : ref,
                                'kakao_img' :kakao_img
                            }
                            news_info.append(data)

                        except TypeError:
                            print("TypeError", title)
                            pass
                        except AttributeError:
                            print('AttributeError', title)
                            pass
                        print('Success', title)

    return news_info


# Dict형태로 변환 함수
def dict_infor(**kwargs):
    context = {}
    for k,v in kwargs.items():
        context[k] = v
    return context
# , 'politics', 'economic', 'foreign', 'culture', 'digital', 'entertain', 'sports'

def parse_daum():
    # insight_news_info = None
    category_list = ['society','economic','politics', 'economic', 'foreign', 'culture', 'digital', 'entertain', 'sports']
    data_list = []
    # i = 0
    for category in category_list:
        for num in range(1,2):
            print(f'{category} - {num} 페이지 스크래핑 시작 -!')
            date = datetime.today().strftime("%Y%m%d")
            response = requests.get(f'https://news.daum.net/breakingnews/{category}?page={num}&regDate={date}')
            soup = BeautifulSoup(response.text, 'html.parser')
            
            ul = soup.select_one('#mArticle > div.box_etc > ul')
            lis = ul.select('li')
            
            for li in lis:
                try:
                    title = li.select_one('div > strong > a').text
                    ref = li.select_one('div > strong > a')['href']
                    code = ref.split('/')[4]
                    press = li.select_one('strong > span').text
                    press = press.split('·')
                    press = press[0].strip()
                    preview_img = li.select_one('a > img')['src']
                    detail_ul = soup.select_one('#mArticle > ul')
                    detail_li = detail_ul.select_one('li.on > a').text.replace('선택됨','').replace('\n','').strip()

                    news_url = requests.get(ref)
                    news_url_html = BeautifulSoup(news_url.text, 'html.parser')

                    date = news_url_html.select_one('#cSub > div > span > span > span').text
                    date = date.strip()
                    date_list = date.replace(' ','.').split('.')
                    date_list = ' '.join(date_list).split()
                    date_list = date_list[0]+'-'+date_list[1]+'-'+date_list[2]+' '+date_list[3]
                    date_code = datetime.strptime(date_list,'%Y-%m-%d %H:%M')
                    kakao_img = news_url_html.select_one('#harmonyContainer > section > figure > p > img')['src']
                    timestamp = time.mktime(date_code.timetuple())
                    timestamp = str(timestamp)
                    content = news_url_html.select_one('#harmonyContainer > section')
                    context = dict_infor(press=press,news_code=code, news_category=detail_li, date=date_code, preview_img=preview_img, title=title, content=str(content),ref=ref, created_at = timestamp, kakao_img=kakao_img)
                    data_list.append(context)
                    
                except TypeError:
                    print('TypeError', title)
                    pass
                
                print('Success', title)
    
    return data_list
