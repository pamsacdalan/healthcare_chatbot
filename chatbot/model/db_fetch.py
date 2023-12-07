import requests
import psycopg2
from dotenv import dotenv_values

# loading the credentials
db_creds = dotenv_values("app/.env")
host = db_creds['URL']
user = db_creds['USER']
password = db_creds['PASSWORD']
dbname = db_creds['DB']


def text_to_sql(prompt):
    '''Function to convert natural language to sql and query the db.
        Accepts prompt as parameter'''
    
    # query api using prompt and context
    context = "CREATE TABLE app_dentist ( id int8, dentist_name varchar(128) NULL, clinic_name varchar(500) NULL, address varchar(500) NULL, city_town varchar(500) NULL, province varchar(500) NULL, region varchar(500) NULL, zip_code int4 NULL, contact_number varchar(128) NULL, monday_start int4 NULL, monday_end int4 NULL, tuesday_start int4 NULL, tuesday_end int4 NULL, wednesday_start int4 NULL, wednesday_end int4 NULL, thursday_start int4 NULL, thursday_end int4 NULL, friday_start int4 NULL, friday_end int4 NULL, saturday_start int4 NULL, saturday_end int4 NULL, sunday_start int4 NULL, sunday_end int4 NULL, );"
    payload= {'prompt':prompt, 'schema':context}
    response = requests.post('https://www.eversql.com/api/generateSQLFromText/',data=payload)
    
    # get the converted sql query
    sql_query = response.text.replace("\\n"," ").replace('"',"")

    # fetch data from db using the generated sql query
    conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=password)
    cur = conn.cursor()
    try:
        cur.execute(sql_query)
        ans = cur.fetchall()
    except:
        ans = "Error fetching database using the query. Please try another query."
    return ans

# prompt = "List dentists who are available on both Tuesdays and Thursdays along with their contact numbers."
# print(text_to_sql(prompt))