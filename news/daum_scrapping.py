import requests
from bs4 import BeautifulSoup
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/app')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from django.db.models import Q 
from user.models import User
from news.models import Article, Potal,Press,Category, UserPress
from datetime import datetime
from social.models import Like

import time



"""
author: son hee jung
date: 0717
description:
daum 뉴스 페이지 카테고리별로 하루치 스크래핑 하는 함수, 카테고리 따로 리스트 받아서 for문을 돌림
코드 리팩토링 필요함(코드 정리, 함수 class로 변경가능?)
"""

insight_news_info = []

# Dict형태로 변환 함수
def dict_infor(**kwargs):
    context = {}
    for k,v in kwargs.items():
        context[k] = v
    return context

# , 'politics', 'economic', 'foreign', 'culture', 'digital', 'entertain', 'sports'
category_list = ['economic','society']

def parse_daum():
    data = {}
    i = 0
    for category in category_list:
        for num in range(1,2):
            time.sleep(5)
            print(f'{category} - {num} 페이지 스크래핑 시작 -!')
            date = datetime.today().strftime("%Y%m%d")
            response = requests.get(f'https://news.daum.net/breakingnews/{category}?page={num}&regDate={date}')
            soup = BeautifulSoup(response.text, 'html.parser')
    #         category = bg.select_one('#kakaoGnb > div > ul > li.on > a > span.ir_wa')
            ul = soup.select_one('#mArticle > div.box_etc > ul')
            lis = ul.select('ul > li')
            for li in lis:
                try:
                    title = li.select_one('div > strong > a').text
                    ref = li.select_one('div > strong > a')['href']
                    code = ref.split('/')[4]
    #                 print(code)
                    press = li.select_one('strong > span').text
                    press = press.split('·')
                    press = press[0]
                    preview_img = li.select_one('a > img')['src']
                    news_url = requests.get(ref)
                    news_url_html = BeautifulSoup(news_url.text, 'html.parser')
                    detail_ul = soup.select_one('#mArticle > ul')
                    detail_li = detail_ul.select_one('#mArticle > ul > li.on > a').text.replace('선택됨','').replace('\n','')
                    print(detail_li)
                    # category_word = news_url_html.select_one('#mArticle > ul > li.on > a > span').text
                    # print(category_word)
                    date = news_url_html.select_one('#cSub > div > span > span > span').text
                    date = date.strip()
                    date_list = date.replace(' ','.').split('.')
                    date_list = ' '.join(date_list).split()
                    date_list = date_list[0]+'-'+date_list[1]+'-'+date_list[2]+' '+date_list[3]
                    date_code = datetime.strptime(date_list,'%Y-%m-%d %H:%M')
                    print(date_code)
                    timestamp = time.mktime(date_code.timetuple())
                    timestamp = str(timestamp)
    #                 print(timestamp)
                    content = news_url_html.select_one('#harmonyContainer > section')
                    content = str(content)
                except TypeError:
                    print('error')
                    pass
                # print(insight_news_info)
                insight_news_info = dict_infor( press=press,news_code=code, news_category=detail_li, date=date_code, preview_img=preview_img, title=title, content=content,ref=ref, created_at = timestamp)
                # print(insight_news_info) 
                i += 1
                data[i] = insight_news_info
    return data

if __name__=='__main__':
    press_list = ['KBS','MBC','경향신문','MBN','SBS','국민일보','노컷뉴스','뉴시스','디스패치','동아일보','매일경제','머니투데이','서울경제','서울신문','세계일보','연합뉴스','이데일리','중앙일보','한국경제','머니S','스포츠조선','스포츠투데이','오마이뉴스','YTN','MK스포츠','MBC연예','SBS연예뉴스']
    news_dict = parse_daum()

    for v in news_dict.values():
        if Press.objects.filter(name=v['press']):
            print('27개 안에 들어감',v['press'])
            print('여기까지는 성고오오오오오옹')
            
            if not Article.objects.filter(Q(title=v['title']) | Q(content=v['content'])):
                article = Article.objects.create(
                    press=Press.objects.filter(name=v['press']).first(),
                    potal = Potal.objects.filter(name='다음').first(),
                    category=Category.objects.filter(name=v['news_category']).first(),
                    code=v['news_code'],
                    date=v['date'],
                    preview_img=v['preview_img'],
                    title=v['title'],
                    content=v['content'],
                    ref=v['ref'],
                    counted_at = 0,
                    created_at = v['created_at']
                        )

                if not Like.objects.filter(article = article):
                    Like.objects.create(
                    article=article
                    )
            # press userpress에 없을경우 추가해준다 
            # press_obj = Press.objects.filter(name = v['press']).first()
            # userpress_list = UserPress.objects.all()
            # for userpress in userpress_list:
            #     if press_obj not in userpress.press.all():
            #         userpress.press.add(press_obj)

              
    # except:
        # pass