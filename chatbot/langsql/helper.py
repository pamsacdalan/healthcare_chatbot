from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import HuggingFaceHub
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
from dotenv import load_dotenv
import sqlite3
from datetime import date
import calendar
import prompts


# FEEDING FEW SHOT PROMPTS TO THE LLM
def generate_prompt():
    # load environment variables
    load_dotenv()

    # few shot prompts
    examples_query = prompts.examples

    example_query_prompt = PromptTemplate(
        input_variables=["input", "sql_cmd"],
        template="\nQuestion: {input}\nSQLQuery: {sql_cmd}",
    )

    # vectorizing the prompts and adding to vectorstore
    embeddings = HuggingFaceEmbeddings()

    to_vectorize = [" ".join(example.values()) for example in examples_query]

    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples_query)

    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=1,
    )

    # accessing current weekday and user's location
    curr_date = date.today()
    day_today = calendar.day_name[curr_date.weekday()]
    location = "" # use User's location

    # passing initial prompt to llm
    custom_sql_prompt = prompts.custom_sql_query

    if location == "":
        custom_sql_prompt = custom_sql_prompt.replace("{day}",day_today)
    else:
        custom_sql_prompt = custom_sql_prompt.replace("{day}",day_today).replace("None",location)


    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_query_prompt,
        prefix= custom_sql_prompt, #change to custom prompt
        suffix=PROMPT_SUFFIX, 
        input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
    )

    ## return generated few shot prompts
    return few_shot_prompt


def create_chain(prompt):
    llm = HuggingFaceHub(repo_id='tiiuae/falcon-7b-instruct')
    dentist_db = 'dentist_test_db.sqlite'
    sql_db = SQLDatabase.from_uri(f'sqlite:///{dentist_db}')
    query_chain = SQLDatabaseChain.from_llm(llm, db=sql_db, prompt=prompt, return_sql=True)
    return query_chain


def get_query(resp_dict):
    # get the sql from chain's response
    try:
        sql_query = resp_dict['result'].split('\n',1)[0].strip()
        return sql_query
    except:
        return resp_dict


def query_db(query):
    dentist_db = 'dentist_test_db.sqlite'

    conn = sqlite3.connect(dentist_db)
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        return e
    finally:
        conn.close()