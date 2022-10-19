# sdk : software development kit, 軟體開發套件

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('hKDvq+jYjOVGi6mJF7cLZeC1PF0ZSguwsetOEUHXYpY3TjbFNRwApoMJciwHH9kUO/Vqt5gE631JKdZRYSpgd+jPVGCWURiA6YRcPgUZayvuhwhkr5q9x3YiJ2jSkzVOv4Gg1pB0TluwzY3l7cgByAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('218abb73247188e9a2c744277698cb47')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()