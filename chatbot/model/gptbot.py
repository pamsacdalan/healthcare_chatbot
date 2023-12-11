import os
from chatbot.model import constants
from chatbot.model.db_fetch import text_to_sql
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from dotenv import dotenv_values

# loading the credentials
db_creds = dotenv_values("app/.env")
api_key = db_creds['OPENAI_API_KEY']
os.environ["OPENAI_API_KEY"] = api_key

loader = TextLoader("./dataset/gpt_traindata.txt")
index = VectorstoreIndexCreator().from_loaders([loader])

def gptbot(sentence:str):
    return index.query("Answer this in 3 sentences or less:" + sentence, llm=ChatOpenAI(model_name="gpt-3.5-turbo"))

#print(gptbot("Who are you?"))
#print(gptbot("I have a toothache, do you recommend seeing a dentist?"))
#print(gptbot("Where can I see your dentists?"))