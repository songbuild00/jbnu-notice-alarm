#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import nextcord
from nextcord.ext import commands, tasks
import random
from dotenv import load_dotenv

load_dotenv()

client = nextcord.Client()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_SLEEP_TIME = 3;

GUILD_ID = os.environ.get("GUILD_ID")
NOTICE_CHANNEL_ID = os.environ.get("NOTICE_CHANNEL_ID")
CS_CHANNEL_ID = os.environ.get("CS_CHANNEL_ID")
CSAI_CHANNEL_ID_1 = os.environ.get("CSAI_CHANNEL_ID_1")
CSAI_CHANNEL_ID_2 = os.environ.get("CSAI_CHANNEL_ID_2")
CSAI_CHANNEL_ID_3 = os.environ.get("CSAI_CHANNEL_ID_3")

DISCORD_API_KEY = os.environ.get("DISCORD_API_KEY")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.151 Whale/3.14.134.62 Safari/537.36",
    "Referer": "https://www.jbnu.ac.kr/kor/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}

async def jbnu_notice():
    now = datetime.now()
    print("start notice check! ", now.strftime('%Y-%m-%d %H:%M'))
    before_notice = 0
    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
        before_notice = int(f_read.readline())
        f_read.close()

    notice_list = []
    latest_notice = 0
    
    for i in range(3):
        try:
            time.sleep(random.randint(1, MAX_SLEEP_TIME))
            req = requests.get('http://www.jbnu.ac.kr/kor/?menuID=139&pno=' + str(i + 1), headers=headers, timeout=30)
            req.encoding = 'utf-8'

            soup = BeautifulSoup(req.text, 'html.parser')
            table = soup.find('table', {'class': 'ta_bo'})
            tbody = table.find("tbody")
            tr_list = tbody.find_all("tr")
            for tr in tr_list:
                notice_number = int(tr.find('td', {'class': 'left'}).find('a')['href'].split('=')[-1])
                if latest_notice < notice_number:
                    latest_notice = notice_number
                if notice_number <= before_notice:
                    if tr.find('th').find('img') is None:
                        break;
                    else:
                        continue;
                td_list = tr.find_all('td')
                notice_group = td_list[0].find('span').get_text().strip()
                notice_subject = td_list[1].find('a').get_text().strip()
                notice_author = td_list[3].find('span')['title']
                notice_date = td_list[4].get_text().strip()
            
                notice_list.append([notice_number, notice_group, notice_subject, notice_author, notice_date])
                print(f"{notice_number}. {notice_group}: {notice_subject} - {notice_author} ({notice_date})")
        except Exception as e:
            print("Exception Error!", e)
            notice_list = []
            break

    if notice_list:
        notice_list.reverse()
        guild = client.get_guild(GUILD_ID)
        if guild is None:
            print("guild is None!")
            return
        channel = guild.get_channel(NOTICE_CHANNEL_ID)
        for notice in notice_list:
            embed = nextcord.Embed(title=notice[2], colour=nextcord.Colour.dark_purple())
            embed.set_author(name=notice[1], url="https://www.jbnu.ac.kr/kor/", icon_url="https://www.jbnu.ac.kr/kor/images/jbnu_144.png")
            embed.url = "https://www.jbnu.ac.kr/kor/?menuID=139&mode=view&no=" + str(notice[0])
            embed.description = notice[3] + " (" + notice[4] + ")"
            embed.set_footer(text="공지번호: " + str(notice[0]))
            await channel.send(embed=embed)
            
        with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
            f_write.write(str(latest_notice))
            f_write.close()
            print("latest.txt edited!")
    else:
        print("No new notice.")

async def jbnu_csai_notice(board_num, channel_num, notice_name):
    now = datetime.now()
    print("start csai notice check! ", board_num, now.strftime('%Y-%m-%d %H:%M'))
    before_notice = 0
    file_name = "latest_csai_" + str(board_num) + ".txt"
    with open(os.path.join(BASE_DIR, file_name), 'r+') as f_read:
        before_notice = int(f_read.readline())
        f_read.close()

    notice_list = []
    latest_notice = 0
    
    try:
        req = requests.get('https://csai.jbnu.ac.kr/csai/' + str(board_num) + '/subview.do', headers=headers, timeout=30)
        req.encoding = 'utf-8'

        soup = BeautifulSoup(req.text, 'html.parser')
        table = soup.find('table', {'class': 'artclTable artclHorNum1'})
        tbody = table.find("tbody")
        tr_list = tbody.find_all("tr")
        for tr in tr_list:
            if len(tr['class']) > 0:
                continue
            td_list = tr.find_all('td')
            notice_number = int(td_list[0].get_text())
            if latest_notice < notice_number:
                latest_notice = notice_number
            if notice_number <= before_notice:
                break
            notice_subject = td_list[1].find('a').find('strong').get_text()
            notice_link = td_list[1].find('a')['href']
            notice_author = td_list[2].get_text().strip()
            notice_date = td_list[3].get_text()
            notice_list.append([notice_number, notice_subject, notice_author, notice_date, notice_link])
            print(f"{notice_number}. {notice_subject} - {notice_author} ({notice_date}), {notice_link}")
    except Exception as e:
        print("Exception Error!", e)
        notice_list = []

    if notice_list:
        notice_list.reverse()
        guild = client.get_guild(GUILD_ID)
        if guild is None:
            print("guild is None!")
            return
        channel = guild.get_channel(channel_num)
        for notice in notice_list:
            embed = nextcord.Embed(title=notice[1], colour=nextcord.Colour.dark_blue())
            embed.set_author(name=notice_name, url="https://csai.jbnu.ac.kr/csai/index.do", icon_url="https://www.jbnu.ac.kr/kor/images/227_5.jpg")
            embed.url = "https://csai.jbnu.ac.kr" + notice[4]
            embed.description = notice[2] + " (" + notice[3] + ")"
            embed.set_footer(text="공지번호: " + str(notice[0]))
            await channel.send(embed=embed)

        with open(os.path.join(BASE_DIR, file_name), 'w+') as f_write:
            f_write.write(str(latest_notice))
            f_write.close()
            print(file_name + " edited!")
    else:
        print("No new csai notice.")

@client.event
async def on_ready():
    await jbnu_notice()
    await jbnu_csai_notice(29107, CSAI_CHANNEL_ID_1, "학사 공지")
    await jbnu_csai_notice(29108, CSAI_CHANNEL_ID_2, "취업 정보")
    await jbnu_csai_notice(29106, CSAI_CHANNEL_ID_3, "일반 공지")
    await client.close()

if __name__ == '__main__':
    client.run(DISCORD_API_KEY)
