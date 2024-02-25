# jbnu-notice-alarm
전북대학교의 최신 공지를 파악하여 디스코드 봇으로 메시지를 보내주는 프로그램입니다. 기존에는 1시간마다 정리하여 메일로 보내주도록 작성하였으나, 디스코드 봇으로 채널에 메시지를 보내면 자동으로 앱 알림을 받을 수 있어 이 방법으로 변경하였습니다. 공지의 제목과 올린 날짜, 올린 사람 이름을 같이 embed 형식의 메시지로 보내주고, 해당 메시지를 클릭하면 메시지에 맞는 공지 페이지를 열어 확인할 수 있도록 url 연결을 하였습니다.

---

## 세팅 방법
* .env 파일에 GUILD_ID, NOTICE_CHANNEL_ID, CSAI_CHANNEL_ID_1, CSAI_CHANNEL_ID_2, CSAI_CHANNEL_ID_3, DISCORD_API_KEY 를 본인의 [디스코드 봇](https://discord.com/developers/applications)에 맞춰 적습니다.
* [latest.txt](https://www.jbnu.ac.kr/kor/?menuID=139), [latest_csai_29106.txt](https://csai.jbnu.ac.kr/csai/29106/subview.do), [latest_csai_29107.txt](https://csai.jbnu.ac.kr/csai/29107/subview.do), [latest_csai_29108.txt](https://csai.jbnu.ac.kr/csai/29108/subview.do) 파일을 생성하고 해당 일자의 가장 최신 공지번호를 적습니다.
* 본인의 서버에 crontab을 이용하여 일정 시간마다 main.py를 실행시킵니다.