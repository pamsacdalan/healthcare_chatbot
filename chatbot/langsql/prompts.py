examples = [
    {
        "input": "How many clinics are open on Sunday?",
        "sql_cmd": "SELECT COUNT(*) FROM dentists WHERE 'Sunday_start' IS NOT NULL;",
    },
    {
        "input": "How many clinics are by appointment?",
        "sql_cmd": "SELECT COUNT(*) FROM dentists WHERE by_appointment = 1",
    },
    {
        "input": "How many clinics are open on Monday at 8:00am?",
        "sql_cmd": "SELECT COUNT(*) FROM dentists WHERE Monday_start <= 8;",
    },
    {
        "input": "How many dentists are open at 9:00 am in Caloocan on Monday?",
        "sql_cmd": "SELECT COUNT(*) FROM dentists WHERE citytown LIKE '%caloocan%' OR province LIKE '%caloocan%' OR region LIKE '%caloocan%' AND Monday_start <= 9",
    },
    {
        "input": "Give me 10 clinics in Manila",
        "sql_cmd": "SELECT clinicname FROM dentists WHERE citytown LIKE '%manila%' or province LIKE'%manila%' or region LIKE '%manila%' LIMIT 10;",
     },
    {
        "input": "Give me the contact number of clinic",
        "sql_cmd": "SELECT contactnumber FROM dentists WHERE clinicname LIKE '%clinic%';",
    },
    {
        "input": "What are clinics in Manila that is open on Tuesday",
        "sql_cmd": "SELECT clinicname FROM dentists WHERE citytown LIKE '%manila%' or province LIKE'%manila%' or region LIKE '%manila%' AND Tuesday_start IS NOT NULL;",
     },
]

examples_psql = [
    {
        "input":"How many clinics are open on Sunday?",
        "sql_cmd":"SELECT COUNT(*) FROM app_dentist WHERE Sunday_start IS NOT NULL;"
    },
    {
        "input":"Who are  open on Monday at 8:00am?",
        "sql_cmd":"SELECT dentist_name FROM app_dentist WHERE Monday_start <= 8;"
    },
    {
        "input":"What is the contact number of this dentist?",
        "sql_cmd":"SELECT contact_number FROM app_dentist WHERE dentist_name ILIKE '%this dentist%';"
    },
    {
        "input":"What dentists are open at 9:00am in Caloocan on Monday?",
        "sql_cmd":"SELECT dentist_name FROM app_dentist WHERE city_town ILIKE '%caloocan%' OR province ILIKE '%caloocan%' OR region ILIKE '%caloocan%' AND Monday_start <= 9"
    },
    {
        "input":"Give me 10 clinics in city town",
        "sql_cmd":"SELECT clinic_name FROM app_dentist WHERE city_town ILIKE '%city town%' or province ILIKE'%city town%' or region ILIKE '%city town%' LIMIT 10;"
    },
    {
        "input":"Give me the contact number of clinic",
        "sql_cmd":"SELECT contact_number FROM app_dentist WHERE clinic_name ILIKE '%clinic%';"
    },
    {
        "input":"What are clinics in Manila city that is open on Tuesday?",
        "sql_cmd":"SELECT clinic_name FROM app_dentist WHERE city_town ILIKE '%manila%' or province ILIKE'%manila%' or region ILIKE '%manila%' AND Tuesday_start IS NOT NULL;"
    },
    {
        "input":"What clinics closes is still open at 5pm on Wednesday?",
        "sql_cmd":"SELECT dentist_name FROM app_dentist WHERE wednesday_end >=6"
    },
    {
        "input":"What clinics in Taguig are open on Weekends?",
        "sql_cmd":"SELECT dentist_name FROM app_dentist WHERE saturday_start is not null or sunday_start is not null AND city_town ILIKE '%Taguig%' or province ILIKE '%Taguig%' OR region ILIKE '%Taguig%';"
    },
    {
        "input":"Where is Dr. XYZ located?",
        "sql_cmd":"SELECT address FROM app_dentist WHERE clinic_name ILIKE '%XYZ%' or dentist_name ILIKE '%XYZ%';"
    },
]

custom_sql_query = """You are a SQLite expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use {day}, if the question involves "today". If the location is not specified use None in your query.

    Use the following format:

    Question: Question here
    SQLQuery: SQL Query to run
    """

custom_postgre_prompt = """
"""