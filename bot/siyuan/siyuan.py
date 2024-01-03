from config import conf
from bot.bot import Bot
import requests
import datetime
from wechatpy import create_reply


class siyuanWriter(Bot):
    def __init__(self):
        self.urlbase = conf().get('siyuan_url')
        self.notebook = conf().get('notebook')
        self.apitoken = conf().get('apitoken')
        self.username = conf().get('user_name')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization' : f'Token {self.apitoken}'
        }
        self.headers2 = {
            'Authorization' : f'Token {self.apitoken}'
        }

        # self.urlmd = self.urlbase + '/api/filetree/createDocWithMd'
        # self.urlfile = self.urlbase + '/api/asset/upload'

    def date_time(self, isweek=True):
        weekday_dict = {
        '0': '日',
        '1': '一',
        '2': '二',
        '3': '三',
        '4': '四',
        '5': '五',
        '6': '六'
        }
        now = datetime.datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        weekday = weekday_dict[now.strftime("%w")]
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        second = now.strftime("%S")
        if isweek:
            return f"{year}年{month}月{day}日星期{weekday}-{hour}:{minute}:{second}"
        else:
            return f"{year}-{month}-{day}-{hour}-{minute}-{second}"

    # 消息返回
    def reply(self, query, context=None):
        # return query[-1]
        if query[0] == 'text':
            if query[1].startswith('https://') or query[1].startswith('http://'):
                reply_msg = self.link_note_text(query[1], context)
            elif query[1].startswith('查询'):
                reply_msg = self.search(query[1].replace('查询', ''), context)
            else:
                reply_msg = self.text_note(query[1], context)
        elif query[0]  == 'image':
            reply_msg = self.image_note(query[1], context)
        # elif query[0]  == 'voice':
        #     reply_msg= self.voice_note(query[1], context)
        elif query[0]  == 'location':
            reply_msg = self.location_note(query[1], context)
        elif query[0]  == 'link':
            reply_msg = self.link_note(query[1], context)
        # elif query[0] == 'video':
        #     reply_msg = self.video_note(query[1], context)
        else:
            return '不支持这类消息'
        return reply_msg

     # 定义查询动作       
    def search(self, message, context=None):
        #判断用户openid是否有权限写入笔记本
        # print(self.username)
        if context['from_user_id'] == self.username:
            data = {"stmt": f"SELECT * FROM blocks WHERE content LIKE'%{message}%' and box != '20210808180117-czj9bvb'"}
            url = self.urlbase + '/api/query/sql'
            response = requests.post(url, headers=self.headers, json=data)
            result = response.json()
            if 'code' in result and result['code'] == 0 and len(result['data']) != 0:
                msg_str = ''
                for d in result['data']:
                    msg_str += d['content'] + '\n'
                return msg_str
                # return f"{result['data']}"
            elif len(result['data']) == 0:
                return "没有相关记录"
            else:
                return "查询失败"
        else:
            return f"此用户无权限:{context['from_user_id']}"   



    # 定义收到文本消息的动作       
    def text_note(self, message, context=None):
        #判断用户openid是否有权限写入笔记本
        # print(self.username)
        if context['from_user_id'] == self.username:
            path = self.date_time()
            data = {
            "notebook": self.notebook,
            "path": f"【文字】-{path}",
            "markdown": message #以markdown形式写入到思源笔记
            }
            url = self.urlbase + '/api/filetree/createDocWithMd'
            response = requests.post(url, headers=self.headers, json=data)
            result = response.json()
            if 'code' in result and result['code'] == 0:
                return f"记录成功:{path}"
            else:
                return "记录失败"
        else:
            return f"此用户无权限:{context['from_user_id']}"   

    #收到图片消息时的动作
    def image_note(self, message, context=None):
        # 判断用户openid是否有权限写入笔记本
        if context['from_user_id'] == self.username:
            name = self.date_time(isweek=False)
            # url = "http://127.0.0.1:6806/api/asset/upload" #思源笔记上传文件的api
            url = self.urlbase + '/api/asset/upload'
            file_url = message
            response = requests.get(file_url)
            file_content = response.content
            payload = {
                "assetsDirPath": "/assets/",
                "file[]": (f"{name}.jpg", file_content)
            }
            response = requests.post(url, files=payload, headers=self.headers2)
            data = response.json()
            pathp = data['data']['succMap'][f"{name}.jpg"]
            path = self.date_time()
            print(pathp)
            data = {
                "notebook": self.notebook,
                "path": f"【图片】-{path}",
                "markdown": f"![微信图片{name}]({pathp})" #以markdown形式写入到思源笔记
            }
            response = requests.post(self.urlbase + '/api/filetree/createDocWithMd', headers=self.headers, json=data)
            result = response.json()
            if 'code' in result and result['code'] == 0:
                return f"记录成功:{path}"
            else:
                return "记录失败"
        else:
            return f"此用户无权限:{context['from_user_id']}"

        #收到视频消息时的动作
    def video_note(self, message, context=None):
        # 判断用户openid是否有权限写入笔记本
        if context['from_user_id'] == self.username:
            name = self.date_time(isweek=False)
            # url = "http://127.0.0.1:6806/api/asset/upload" #思源笔记上传文件的api
            url = self.urlbase + '/api/asset/upload'
            file_url = message
            response = requests.get(file_url)
            file_content = response.content
            payload = {
                "assetsDirPath": "/assets/",
                "file[]": (f"{name}.jpg", file_content)
            }
            response = requests.post(url, files=payload, headers=self.headers2)
            data = response.json()
            pathp = data['data']['succMap'][f"{name}.jpg"]
            path = self.date_time()
            data = {
                "notebook": self.notebook,
                "path": f"【图片】-{path}",
                "markdown": f"![微信图片{name}]({pathp})" #以markdown形式写入到思源笔记
            }
            response = requests.post(self.urlbase + '/api/filetree/createDocWithMd', headers=self.headers, json=data)
            result = response.json()
            if 'code' in result and result['code'] == 0:
                return f"记录成功:{path}"
            else:
                return "记录失败"
        else:
            return f"此用户无权限:{context['from_user_id']}"



    # #定义收到语音消息的动作

    # def voice_note(message, session):
    #     #判断用户openid是否有权限写入笔记本
    #     if message.source == openid:
    #         data = {
    #         "notebook": notebook,
    #         "path": f"【语音】-{path}",
    #         "markdown": message.recognition #以markdown形式写入到思源笔记
    #         }
    #         response = requests.post(urlmd, headers=headers, json=data)
    #         result = response.json()
    #         if 'code' in result and result['code'] == 0:
    #             return f"记录成功:{path}"
    #         else:
    #             return "记录失败"
    #     else:
    #         return f"此用户无权限:{message.source}"

    # #定义收到位置消息的动作

    def location_note(self, message, context=None):
        # 判断用户openid是否有权限写入笔记本
        if context['from_user_id'] == self.username:
            path = self.date_time()
            location = message['location']
            scale = message['scale']
            latitude = str(message['location_x'])
            longitude = str(message['location_y'])
            location_link = f"https://ditu.amap.com/regeo?lng={longitude}&lat={latitude}"
            data = {
            "notebook": self.notebook,
            "path": f"【位置】-{path}",
            "markdown": f"经度：{latitude}\n纬度：{longitude}\n放缩倍数：{scale}\n地点：[{message['label']}]({location_link})" #以markdown形式写入到思源笔记
            }
            response = requests.post(self.urlbase + '/api/filetree/createDocWithMd', headers=self.headers, json=data)
            result = response.json()
            if 'code' in result and result['code'] == 0:
                return f"记录成功:{path}"
            else:
                return "记录失败"
        else:
            return f"此用户无权限:{context['from_user_id']}"

    #定义收到链接消息的动作

    def link_note(self, message, context=None):
        # 判断用户openid是否有权限写入笔记本
        if context['from_user_id'] == self.username:
            path = self.date_time()
            data = {
            "notebook": self.notebook,
            "path": f"【链接】-{path}",
            "markdown": f"链接：[{message['title']}]({message['url']})\n标题：{message['title']}\n描述：{message['description']}" #以markdown形式写入到思源笔记
            }
            response = requests.post(self.urlbase + '/api/filetree/createDocWithMd', headers=self.headers, json=data)
            result = response.json()
            if 'code' in result and result['code'] == 0:
                return f"记录成功:{path}"
            else:
                return "记录失败"
        else:
            return f"此用户无权限:{context['from_user_id']}"

    # 定义收到只有一个链接的消息
    def link_note_text(self, message, context=None):
        # 判断用户openid是否有权限写入笔记本
        if context['from_user_id'] == self.username:
            path = self.date_time()
            data = {
            "notebook": self.notebook,
            "path": f"【链接】-{path}",
            "markdown": f"链接：[{message}]({message})\n" #以markdown形式写入到思源笔记
            }
            response = requests.post(self.urlbase + '/api/filetree/createDocWithMd', headers=self.headers, json=data)
            result = response.json()
            if 'code' in result and result['code'] == 0:
                return f"记录成功:{path}"
            else:
                return "记录失败"
        else:
            return f"此用户无权限:{context['from_user_id']}"