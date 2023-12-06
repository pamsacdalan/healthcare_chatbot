import os
import constants
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY
loader = TextLoader("./dataset/gpt_traindata.txt")
index = VectorstoreIndexCreator().from_loaders([loader])

def gptbot(sentence:str):
    return index.query(sentence, llm=ChatOpenAI(model_name="gpt-3.5-turbo"))

#print(gptbot("Who are you?"))
#print(gptbot("I have a toothache, do you recommend seeing a dentist?"))
print(gptbot("Where can I see your dentists?"))