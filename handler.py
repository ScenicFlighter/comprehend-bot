# -*- coding: utf-8 -*-

import os
import sys
import logging
import json
import boto3

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# 翻訳
translate = boto3.client('translate')
# 言語処理
comprehend = boto3.client('comprehend')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def bot_hook(event, context):
    
    line_event = json.loads(event['body'])['events'][0]
    
    logger.info(line_event)

    # 引数テキストを英語変換
    trans = translate.translate_text(
        Text=line_event['message']['text'],
        SourceLanguageCode='auto',
        TargetLanguageCode='en'
    )

    translatedText = trans['TranslatedText']
    
    logger.info(translatedText)

    # 感情表現を取得
    detect_sentiment = comprehend.batch_detect_sentiment(
        TextList = [
            translatedText
        ],
        LanguageCode='en'
    )

    logger.info(detect_sentiment)
    logger.info(detect_sentiment['ResultList'][0]['Sentiment'])

    sentiment = detect_sentiment['ResultList'][0]['Sentiment']

    line_bot_api.reply_message(
        line_event['replyToken'],
        TextSendMessage(text=sentiment)
    )

    response = {
        "statusCode": 200
    }

    return response
