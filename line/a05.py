from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


line_bot_api = LineBotApi('LINE_CHANNEL_ACCESS_TOKEN')
line_handler = WebhookHandler('LINE_CHANNEL_SECRET')


from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api.push_message('XXXX', TextSendMessage(text='Hello World!!!'))