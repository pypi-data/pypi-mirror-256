import requests,json,time,http.client,random,string,sys #NOMAL
import urllib.parse,cv2,numpy #RUNQR







# LINE_ACCOUNT_EMAIL='tiktok.asuka.taw@gmail.com'
# LINE_ACCOUNT_PASSWORD='Line123456789'
# LINE_ACCOUNT_MID='Ueef5362e88e6dd8177a026fdc1ad6247'




class LINEOABOT:
    def __init__(self,**kwargs):
        for key, value in kwargs.items():
            print("%s == %s" % (key, value))
        self.email = kwargs['email']
        self.password = kwargs['password']
        self.mid = kwargs['botid']
        self.defaultHeaders = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en-US,en;q=0.9",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
        }
        self.session = requests.session()
        self.tempData = {}
        self.loginWithEmail()

    def loginWithEmail(self):
        csrfToken = (
            self.session.get(
                url="https://account.line.biz/login?redirectUri=https%3A%2F%2Fchat.line.biz%2F",
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Connection": "keep-alive",
                    "Host": "account.line.biz",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
                },
                data=None,
                allow_redirects=True,
            ).text.split('name="x-csrf" content="')[1].split('"')[0]
        )

        loginResult = self.session.post(
            url="https://account.line.biz/api/login/email",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Content-Type": "application/json;charset=UTF-8",
                "Host": "account.line.biz",
                "Origin": "https://account.line.biz",
                "Referer": "https://account.line.biz/login?redirectUri=https%3A%2F%2Fchat.line.biz%2F",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
                "X-XSRF-TOKEN": csrfToken,
            },
            json={"email": self.email, "password": self.password, "stayLoggedIn": False},
        )

        if loginResult.status_code != 200:
            sys.exit(f"Login Failed, Status Code: {loginResult.status_code}, Error: {loginResult.text}")

        # accessToken = loginResult.headers["Set-Cookie"].split(";")[0].replace("__Host-ses-account=", "")
        # print(accessToken)
        self.getCsrfToken()
        getOwner = self.getOwners()
        check = self.getChatMode()
        getBot = self.getBots()
        msgx = 'Current Setting'
        if 'code' in check:
            print("[ ERROR ] Please set bot to chat mode!!!")
            sys.exit()
        msgx += f'current:{check["current"]}\n'
        msgx += f'- Setting -\n'
        msgx += f'IsBusinessHoursEnabled:{check["setting"]["isBusinessHoursEnabled"]}\n'
        msgx += f'IsInBusinessHours:{check["setting"]["isInBusinessHours"]}\n'
        msgx += f'ChatModeInBusinessHours:{check["setting"]["chatModeInBusinessHours"]}\n'
        msgx += f'chatModeOutsideBusinessHours:{check["setting"]["chatModeOutsideBusinessHours"]}\n'
        msgx += f'\n'
        msgx += f'- OWNER LISTS -\n'
        msgx += f'\n'
        onum = 1
        for Owner in getOwner:
            msgx += f'{onum}. {Owner["name"]}\n'
            onum += 1
        msgx += f'\n'
        msgx += f'- BOTS LISTS -\n'
        msgx += f'\n'
        bnum = 1
        for bot in getBot:
            msgx += f'{bnum}. {bot["name"]}\n'
            bnum += 1

        print(msgx)
        print("[ LINE OA ] Success login...")

    def getCsrfToken(self):
        _csrf = json.loads(
            self.session.get(
                url="https://chat.line.biz/api/v1/csrfToken",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )["token"]
        self.defaultHeaders["x-xsrf-token"] = _csrf

    def getChatMode(self):
        return json.loads(
            self.session.get(
                url="https://chat.line.biz/api/v3/bots/" + self.mid + "/settings/chatMode",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )

    def getOwners(self):
        return json.loads(
            self.session.get(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/owners",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )["list"]

    def getBots(self):
        return json.loads(
            self.session.get(
                url="https://chat.line.biz/api/v1/bots?noFilter=true&limit=1000",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )["list"]

    def getMessages(self, chatId):
        """
        รับกิจกรรมการสนทนา (ข้อความที่ส่ง ได้รับข้อความ อ่านแล้ว ฯลฯ เป็นกิจกรรมทั้งหมด) \n
        การแสดงเริ่มต้นคือ 50 เหตุการณ์
        """
        return json.loads(
            self.session.get(
                url="https://chat.line.biz/api/v2/bots/" + self.mid + "/messages/" + chatId,
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )["list"]

    def getImageMessages(self, chatId):
        return json.loads(
            self.session.get(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/messages/" + chatId + "/swipeViewer",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )["list"]

    def getMediaInfo(self, messageId):
        return json.loads(
            self.session.get(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/messages/content/" + messageId + "/info",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )

    def getChat(self, chatId):
        """
        รับข้อมูลโดยละเอียดเกี่ยวกับ chatId นี้ \n
        เช่น อ่านแล้ว ชื่อ สถานะ ฯลฯ
        """
        return json.loads(
            self.session.get(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/chats/" + chatId,
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )

    def getChatList(self, folderType="ALL"):  # ['NONE', 'ALL', 'INBOX', 'UNREAD', 'FOLLOW_UP', 'DONE', 'SPAM']
        """
        `folderType = 'NONE', 'ALL', 'INBOX', 'UNREAD', 'FOLLOW_UP', 'DONE', 'SPAM'`\n
        รับ 25 แชท
        """
        return json.loads(
            self.session.get(
                url="https://chat.line.biz/api/v2/bots/" + self.mid + "/chats?folderType=" + folderType + "&tagIds=&limit=25",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )

    def markAsRead(self, chatId, messageId):
        """
        ทำเครื่องหมายแชทเฉพาะว่าอ่านแล้ว \n
        ต้องส่งรหัสข้อความ
        """
        data = {"messageId": messageId}
        return json.loads(
            self.session.put(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/chats/" + chatId + "/markAsRead",
                headers=self.defaultHeaders,
                json=data,
                allow_redirects=True,
            ).text
        )

    def addFollowedUp(self, chatId):
        return json.loads(
            self.session.put(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/chats/" + chatId + "/followUp",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )

    def deleteFollowedUp(self, chatId):
        return json.loads(
            self.session.delete(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/chats/" + chatId + "/followUp",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )

    def addResolved(self, chatId):
        return json.loads(
            self.session.put(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/chats/" + chatId + "/done",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )

    def deleteResolved(self, chatId):
        return json.loads(
            self.session.delete(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/chats/" + chatId + "/done",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )

    def addSpam(self, chatId):
        return json.loads(
            self.session.put(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/chats/" + chatId + "/spam",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )

    def deleteSpam(self, chatId):
        return json.loads(
            self.session.delete(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/chats/" + chatId + "/spam",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )

    def getManualChatStatus(self, chatId):
        return json.loads(
            self.session.get(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/chats/" + chatId + "/useManualChat",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )

    def leaveChat(self, chatId):
        return json.loads(
            self.session.post(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/chats/" + chatId + "/leave",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )

    def deleteChat(self, chatId):
        return json.loads(
            self.session.delete(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/chats/" + chatId,
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )

    def getContactList(self):
        return json.loads(
            self.session.get(
                url="https://chat.line.biz/api/v1/bots/"
                + self.mid
                + "/contacts?query=&sortKey=DISPLAY_NAME&sortOrder=ASC&excludeSpam=true&limit=100",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )["list"]

    def getMembersOfChat(self, chatId):
        return json.loads(
            self.session.get(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/chats/" + chatId + "/members?limit=100",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )["list"]

    def sendMessage(self, chatId, text):
        data = {
            "type": "text",
            "text": text,
            "sendId": chatId + "_" + str(int(time.time())) + "_" + "".join(random.choice(string.digits) for i in range(8)),
        }
        return json.loads(
            self.session.post(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/messages/" + chatId + "/send",
                headers=self.defaultHeaders,
                json=data,
                allow_redirects=True,
            ).text
        )

    def sendSticker(self, chatId, packageId, stickerId):
        data = {
            "stickerId": stickerId,
            "packageId": packageId,
            "type": "sticker",
            "sendId": chatId + "_" + str(int(time.time())) + "_" + "".join(random.choice(string.digits) for i in range(8)),
        }
        return json.loads(
            self.session.post(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/messages/" + chatId + "/send",
                headers=self.defaultHeaders,
                json=data,
                allow_redirects=True,
            ).text
        )

    def sendFileWithPath(self, chatId, path):
        data = {
            "file": open(path, "rb"),
            "sendId": (
                None,
                chatId + "_" + str(int(time.time())) + "_" + "".join(random.choice(string.digits) for i in range(8)),
            ),
        }
        return json.loads(
            self.session.post(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/messages/" + chatId + "/sendFile",
                headers=self.defaultHeaders,
                files=data,
                allow_redirects=True,
            ).text
        )

    def generateContentHashUrl(self, contentHash):
        return "https://chat-content.line-scdn.net/bot/" + self.mid + "/" + contentHash

    def streamingApiToken(self):
        return json.loads(
            self.session.post(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/streamingApiToken",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )





    def openPolling(self, ping=33):
        dataStream = self.streamingApiToken()
        print(dataStream)
        streamingApiToken = dataStream["streamingApiToken"]
        lastEventId = dataStream["lastEventId"]
        lastEventTimestamp = dataStream["lastEventTimestamp"]
        poll = http.client.HTTPSConnection("chat-streaming-api.line.biz")
        poll.request(
            "GET",
            "/api/v2/sse?token="
            + streamingApiToken
            + "&deviceToken=&deviceType=&clientType=PC&pingSecs="
            + str(ping)
            + "&lastEventId="
            + lastEventId,
            headers=self.defaultHeaders,
        )
        return poll

    def changeNickname(self, chatId: str, nickname: str):
        """
        เปลี่ยนชื่อเล่นของผู้ใช้
        """
        payload = {"nickname": nickname}
        return json.loads(
            self.session.put(
                url="https://chat.line.biz/api/v1/bots/" + self.mid + "/chats/" + chatId + "/nickname",
                headers=self.defaultHeaders,
                json=payload,
                allow_redirects=True,
            ).text
        )

    def pinMessage(self, chatId: str, messageId: str):
        """
        ปักหมุดข้อความเฉพาะ
        """
        payload = {"messageId": messageId}
        return self.session.post(
            url="https://chat.line.biz/api/v1/bots/" + self.mid + "/messages/" + chatId + "/pin",
            headers=self.defaultHeaders,
            json=payload,
            allow_redirects=True,
        )

    def unpinMessage(self, chatId: str, messageId: str):
        """
        เลิกปักหมุดข้อความเฉพาะ
        """
        payload = {"messageId": messageId}
        return self.session.delete(
            url="https://chat.line.biz/api/v1/bots/" + self.mid + "/messages/" + chatId + "/pin",
            headers=self.defaultHeaders,
            json=payload,
            allow_redirects=True,
        )

    def getPinnedMessage(self, chatId: str):
        """
        รับข้อความที่ปักหมุดไว้ทั้งหมด
        """
        return json.loads(
            self.session.get(
                url="https://chat.line.biz/api/v2/bots/" + self.mid + "/messages/" + chatId + "/pin",
                headers=self.defaultHeaders,
                data=None,
                allow_redirects=True,
            ).text
        )["messages"]
