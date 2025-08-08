
from flask import Flask,request,render_template,jsonify,abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)


token='XXXX'
channel_secret = 'XXXX'
channel_access_token = token
LIFF_ID = 'XXXX'
LIFF_URL = 'XXXX'

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK' 


@app.route('/liff')
def liff():
    return render_template('index.html', liffid = LIFF_ID)


@app.route('/process',methods= ['POST'])
def process():
  pname=request.form['Nname']
  proom = request.form['selroom']
  pdatatime = request.form['datetime']
  output = '名稱:'+ proom+ pname + '份'+ pdatatime
  if  proom and pname and pdatatime:
   return jsonify({'output':'Full Name: ' + output})


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):    
    input_text = event.message.text
    if input_text == '123':
        message = TemplateSendMessage(
                alt_text='按鈕樣板',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png', 
                    title='測試line liff',
                    text='請選擇：',
                    actions=[
                        URITemplateAction(
                            label='連結網頁',
                            uri=LIFF_URL,
                        ),
                    ]
                )
            )
        
        try:
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=input_text))

if __name__ == '__main__':
    app.run()