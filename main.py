import os, json
import calendar
from datetime import datetime, date, timedelta
from requests_oauthlib import OAuth1Session
#from flask import json, make_response


def tweet_post(text):
    with open('secret.json') as f:
        secret = json.load(f)
        AK = secret['TWIITER_CONSUMER_KEY']
        ASK = secret['TWIITER_CONSUMER_SECRET']
        AT = secret['TWIITER_ACCESS_TOKEN']
        ATS = secret['TWIITER_ACCESS_TOKEN_SECRET']
        EP = secret['TWITTER_ENDPOINT']

    twitter = OAuth1Session(AK, ASK, AT, ATS)
    params = {"status" : text}
    res = twitter.post(EP, params = params)
    if res.status_code == 200: #正常投稿出来た場合
        print("Tweet Success.")
    else: #正常投稿出来なかった場合
        print("Tweet Failed.", res.status_code, res.text)


def calc_fiscal_year(today:datetime)->datetime:
    _uru_year = False
    all_days = 365
    if today.month >= 4: #4月以降なら次年をセット
        end_day = date(year=today.year + 1, month=3, day=31)
        if calendar.isleap(today.year + 1):
            _uru_year = True
    elif today.month < 4:#3月までなら同年をセット
        end_day = date(year=today.year, month=3, day=31)
        if calendar.isleap(today.year):
            _uru_year = True
    else:
        print('error,today.month=', today.month)

    if _uru_year:
        all_days = 366
    
    #残日数を計算
    _remain_days = end_day - today.date()
    remain_days = _remain_days.days
    rate = (remain_days / all_days) * 100

    return remain_days, rate

today = datetime.now() + timedelta(hours=9) + timedelta(minutes=10)
print(today)
remain_days, rate = calc_fiscal_year(today)
tweet_text = f'{today.year}年{today.month}月{today.day}日になりました。今年度は残り{remain_days}日です。あと{round(rate,1)}％です。'
print(tweet_text)

tweet_post(tweet_text)