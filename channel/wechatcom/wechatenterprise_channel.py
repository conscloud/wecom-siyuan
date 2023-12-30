# encoding:utf-8

"""
WechatEnterprise channel
"""
from channel.channel import Channel
from concurrent.futures import ThreadPoolExecutor
from common.log import logger
from config import conf
import json
import requests
import io
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.enterprise import WeChatClient
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.enterprise.exceptions import InvalidCorpIdException
from wechatpy.enterprise import parse_message
from flask import Flask, request ,abort


thread_pool = ThreadPoolExecutor(max_workers=8)
app = Flask(__name__)


@app.route('/wechat', methods=['GET','POST'])
def handler_msg():
    return WechatEnterpriseChannel().handle()

class WechatEnterpriseChannel(Channel):
    def __init__(self):
        self.CorpId = conf().get('WECHAT_CORP_ID')
        self.Secret = conf().get('Secret')
        self.AppId = conf().get('AppId')
        self.TOKEN = conf().get('WECHAT_TOKEN')
        self.EncodingAESKey = conf().get('WECHAT_ENCODING_AES_KEY')
        self.crypto = WeChatCrypto(self.TOKEN, self.EncodingAESKey, self.CorpId)
        self.client = WeChatClient(self.CorpId, self.Secret,self.AppId)

    def startup(self):
        # start message listener
        app.run(host='0.0.0.0',port=3003)

    def send(self, msg, receiver):
        logger.info('[WXCOM] sendMsg={}, receiver={}'.format(msg, receiver))
        self.client.message.send_text(self.AppId,receiver,msg)

    def _do_send(self, query, reply_user_id):
        try:
            if not query:
                return
            context = dict()
            context['from_user_id'] = reply_user_id
            reply_text = super().build_reply_content(query, context)
            if reply_text:
                self.send(reply_text, reply_user_id)
        except Exception as e:
            logger.exception(e)

    def handle(self):
        query_params = request.args
        signature = query_params.get('msg_signature', '')
        timestamp = query_params.get('timestamp', '')
        nonce = query_params.get('nonce', '')    
        if request.method == 'GET':
            # 处理验证请求
            echostr = query_params.get('echostr', '')
            try:
                echostr = self.crypto.check_signature(signature, timestamp, nonce, echostr)
            except InvalidSignatureException:
                abort(403)
            print(echostr)
            return echostr
        elif request.method == 'POST':
            try:
                message = self.crypto.decrypt_message(
                    request.data,
                    signature,
                    timestamp,
                    nonce
                )
            except (InvalidSignatureException, InvalidCorpIdException):
                abort(403)
            msg = parse_message(message)
            # if msg.type == 'image':
            if msg.type == 'text':
                # reply = '收到，马上处理'
                # thread_pool.submit(self._do_send, msg.content, msg.source)
                thread_pool.submit(self._do_send, [msg.type, msg.content], msg.source)
            elif msg.type == 'image':
                # reply = '收到，图片'
                thread_pool.submit(self._do_send, [msg.type, msg.image], msg.source)
            elif msg.type == 'location':
                # reply = '收到， 地址'
                content = {'scale': msg.scale, 
                           'location_x': msg.location_x, 
                           'location_y': msg.location_y, 
                           'label': msg.label,
                           'location': msg.location
                           }
                print(content)
                thread_pool.submit(self._do_send, [msg.type, content], msg.source)
            elif msg.type == 'voice':
                content = {'media_id': msg.media_id, 
                           'format': msg.format, 
                           'recognition': msg.recognition
                           }
                thread_pool.submit(self._do_send, [msg.type, content], msg.source)
            elif msg.type == 'link':
                content = {'title': msg.title, 
                           'description': msg.description, 
                           'url': msg.url
                           }
                thread_pool.submit(self._do_send, [msg.type, content], msg.source)
            # elif msg.type == 'video':
            #     content = {'media_id': msg.media_id,
            #                'thumb_media_id': msg.thumb_media_id}
            #     print(content)
            #     thread_pool.submit(self._do_send, [msg.type, content], msg.source)
            else:
                reply = '暂时不支持这个类型！'
                self.client.message.send_text(self.AppId,msg.source,reply)
            # self.client.message.send_text(self.AppId,msg.source,reply)
            # self.client.message.send_text(self.AppId,msg.source,reply)
            return 'success'
