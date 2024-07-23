import random
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain import hub

def random_number():
    return str(sorted(random.sample(range(1, 46), 6)))


def kospi():
    KOSPI_URL = 'https://finance.naver.com/sise/'

    res = requests.get(KOSPI_URL)
    
    res_text = res.text

    selector = '#KOSPI_now'

    soup = BeautifulSoup(res_text, 'html.parser')
    kospi = soup. select_one(selector).text
    
    return kospi


def openai(api_key, user_input):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': '너는 사용자와 대화하는 챗봇이야'},
            {'role': 'user', 'content': user_input},
        ]
    
    )
    return completion.choices[0].message.content


def langchain(api_key, user_input):
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    # 1. load document(학습할 문서 url)
    loader = WebBaseLoader(
        web_paths=('https://the-edit.co.kr/68178',
        'https://www.apple.com/kr/newsroom/2024/03/apples-worldwide-developers-conference-returns-june-10-2024/'
        ),
    )

    docs = loader.load()

    # 2. split(학습할 문서 나누기)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)

    # 3. store (문서 숫자화)
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=OpenAIEmbeddings()
    )

    # 4. retrieve(검증)
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
    )

    return rag_chain.invoke(user_input)


