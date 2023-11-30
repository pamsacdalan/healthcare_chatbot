from langchain import PromptTemplate, LLMChain
from langchain.llms import CTransformers
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory



# loading the model and defining the memory
llm = CTransformers(model="chatbot\langsql\models\llama-2-7b-chat.Q2_K.gguf", model_type="llama", max_new_tokens=512, temperature=0.1)
memory = ConversationBufferWindowMemory(
    memory_key="history", k=6, return_only_outputs=True
)

# creating the prompt for the chatbot
template = """
You are an AI assistant and your task is to answer user's question and return the answer in a concise way.

Current Conversation:
{history}

Query: {input}

You just return helpful answer and nothing else
Helpful Answer:
""".strip()

prompt = PromptTemplate(input_variables=["history", "input"], template=template)


# Creating a Conversation Chain
chain = ConversationChain(llm=llm, memory=memory, prompt=prompt, verbose=False)



'''
text = "What is an HMO, an how can it help me in my budgetting?"
response = chain.predict(input=text)
print(response)

'''

