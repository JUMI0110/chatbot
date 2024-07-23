from utils import random_number, kospi, openai,langchain
from dotenv import load_dotenv
import requests
import os
from fastapi import FastAPI, Request

load_dotenv()

app = FastAPI()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

@app.post('/')
async def read_root(request: Request): 
    # async 비동기적인처리 요청한 코드의 응답을 기다렸다가 처리  

    body = await request.json()
    
    user_id = body['message']['from']['id']
    user_input = body['message']['text']
    
    if user_input[0] == '/':
        # 우리가 만든 기능 추가
        if user_input == '/lotto':
            text = random_number()
            print(text)

        elif user_input == '/kospi':
            text = kospi()
        else:
            text = '지원하지 않는 기능입니다.'

    else:
        # openAI API 활용
        # text = openai(OPENAI_API_KEY, user_input)
        text = langchain(OPENAI_API_KEY, user_input)


    req_url = f'{URL}/sendMessage?chat_id={user_id}&text={text}'    
        
    requests.get(req_url)
    
    return {'hello': 'world'}