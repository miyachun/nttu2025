from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,StickerSendMessage,ImageMessage,ImageSendMessage,LocationSendMessage
import random
app = Flask(__name__)

line_bot_api = LineBotApi('LINE_CHANNEL_ACCESS_TOKEN')
line_handler = WebhookHandler('LINE_CHANNEL_SECRET')

@app.route('/')
def home():
    return 'Hello World'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'



def myG():
    myW=['你好','吃飽了嗎','天氣如何']
    return random.choice(myW)

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    getA=event.message.text        

    if getA =='0' :        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(myG())))      
    elif getA=='1':
        reply_arr=[]
        reply_arr.append(TextSendMessage(text='111'))
        reply_arr.append(TextSendMessage(text='222'))
        reply_arr.append(TextSendMessage(text='333'))
        reply_arr.append(TextSendMessage(text='444'))
        reply_arr.append(TextSendMessage(text='555'))
        line_bot_api.reply_message(event.reply_token,reply_arr)
    elif getA=='2':
        reply_sticker=StickerSendMessage(
            package_id='1',
            sticker_id='2'
        )
        line_bot_api.reply_message(event.reply_token,reply_sticker)
    elif getA=='3':
        reply_img=ImageSendMessage(
            original_content_url='https://www.nttu.edu.tw/var/file/0/1000/img/1166/Mlogo.jpg',
            preview_image_url='https://www.nttu.edu.tw/var/file/0/1000/img/1166/Mlogo.jpg'
        )
        line_bot_api.reply_message(event.reply_token,reply_img)
    elif getA=='4':
        message=TextSendMessage(
           text="$ hello $ world",
           emojis=[{
            "index":0,
            "productId":"670e0cce840a8236ddd4ee4c",
            "emojiId":"001"

        },
        {
            "index":8,
            "productId":"670e0cce840a8236ddd4ee4c",
            "emojiId":"001"

        }
        ]
        )
     
        
        line_bot_api.reply_message(event.reply_token,message)
    
    elif getA=='5':
        reply_addr=LocationSendMessage(
            title='地址',
            address='台東縣台東市大學路二段369號',
            latitude=22.736767968096814,
            longitude=121.06791480250617
            
        )
        line_bot_api.reply_message(event.reply_token,reply_addr)
    
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="輸入0"))

if __name__ == "__main__":
    app.run()