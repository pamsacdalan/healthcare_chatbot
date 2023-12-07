import psycopg2
import pandas as pd
from datetime import datetime

from dotenv import dotenv_values


# loading the credentials
db_creds = dotenv_values("app\.env")
host = db_creds['HOST']
user = db_creds['USER']
password = db_creds['PASSWORD']
dbname = db_creds['DB']
sslmode=db_creds['SSLMODE']


def paginator(array):
    """This function accepts array and will return a string. Displays only 5 per page. Returns string value of the selected option from array."""

    if len(array) == 5:
        choices = []
        for i in range(len(array)):
            print(f"{i} | {array[i]}")
            choices.append(array[i].lower())

        x = ''
        cont = True
        while cont:
            x = input("Type the number or value to continue")

            if x.lower() == 'q':
                cont = False
                print('Selecting aborted')
                break
            elif type(x) == str and x.lower() in choices:
                print(f'You selected {x}')
                cont = False
                return x.upper()
            else:
                try: 
                    x = int(x)
                    if choices[x] in choices:
                        print(f'You selected {choices[x].upper()}')
                        cont = False
                        return choices[x].upper()
                except:
                    pass

    else:
        n = (len(array) // 5)
        if (len(array) % 5) == 0:
            n_page = n
        else:
            n_page = n + 1

        choices = []
        cur_pos = 0

        for i in range(n_page + 1):
            if i == n_page:
                s = slice(cur_pos, -1)
                sub_choice = array[s]
                choices.append(sub_choice)
            else:
                sub_choice = []
                s = slice(cur_pos, cur_pos+5)
                sub_choice = array[s]
                choices.append(sub_choice)
                cur_pos += 5

        curr_page = 0
        print(f'{curr_page+1}/{n_page} page - {len(array)} options \n')

        for i in range(len(choices[curr_page])):
            print(f"{i} | {choices[curr_page][i]}")

        print("\n")
    
        x = ''
        cont = True
        while cont:
            x = input("Type the number or value to continue. Type 'next page' or 'previous page' to change options.\n")

            if x.lower() == 'q':
                cont = False
                print('Selecting aborted')
                break
            elif x.lower() == 'next page':
                if (len(array) % 5) == 0:
                    if curr_page >= (len(array) // 5) -1:
                        print("This is the last page")
                    elif curr_page < n_page:
                        curr_page += 1
                        print(f'{curr_page+1}/{n_page} page - {len(array)} options \n')

                        for i in range(len(choices[curr_page])):
                            print(f"{i} | {choices[curr_page][i]}")
                        print("\n")
                else:
                    if curr_page >= (len(array) // 5):
                        print("This is the last page")
                    elif curr_page < n_page:
                        curr_page += 1
                        print(f'{curr_page+1}/{n_page} page - {len(array)} options \n')

                        for i in range(len(choices[curr_page])):
                            print(f"{i} | {choices[curr_page][i]}")
                        print("\n")
            elif x.lower() == 'previous page':
                if curr_page > 0:
                    curr_page -= 1
                    print(f'{curr_page+1}/{n_page} page - {len(array)} options \n')

                    for i in range(len(choices[curr_page])):
                        print(f"{i} | {choices[curr_page][i]}")
                    print("\n")
                else:
                    print("This is the first page")
            elif type(x) == str  and x.upper() in choices[curr_page]:
                print(f'You selected {x}')
                cont = False
                return x.upper()
            else:
                try: 
                    x = int(x)
                    if choices[curr_page][x] in choices[curr_page]:
                        print(f'You selected {choices[curr_page][x].upper()}')
                        cont = False
                        return choices[curr_page][x].upper()
                except:
                    pass


def procedure_selector():
    procedure_list = ["Dental Cleanings", "Fillings", "Root Canal Therapy", "Tooth Extraction", "Crowns", "Bridges", "Dental Implants", "Dentures", "Teeth Whitening", "Dental Checkup"]

    procedure = paginator(procedure_list)
    return procedure


import pandas as pd

def city_selector(location):
    """Takes the user's city as parameters. Returns array of dentists based on user's selected city. Also returns city."""
    
    # loading csv
    df = pd.read_csv("chatbot\langsql\converted_functions\dentist_rand_sched_utf.csv")

    while True:
        x = input(f"Current location is {location}. Proceed? Type 'Y' to proceed or type another city.\n")
        
        if x.lower == 'q':
            break
        elif x.lower() == 'y':
            dentists = df.loc[df['city_town'].str.contains(location.lower(),case=False)] # not exact match for now
            return dentists['clinic_name'].values.tolist(), location
        else:
            try:
                dentists = df.loc[df['city_town'].str.contains(x.lower(),case=False)] 
                location = x
            except:
                print("Cannot find dentist in your location. Print another location")
                

def dentist_selector(dentist_list):
    print("Please select a clinic \n")

    dentist = paginator(dentist_list)
    return dentist  


def get_clinic_id(clinic_name, city):
    """Accepts clinic name and city as parameters. Returns id of the said clinic in the selected city."""
    clinic_name = clinic_name.strip()
    # loading csv
    df = pd.read_csv("chatbot\langsql\converted_functions\dentist_rand_sched_utf.csv")
    
    try:
        clinic_id = df.loc[(df['clinic_name'].str.contains(clinic_name.lower(),case=False)) & df['city_town'].str.contains(city.lower(),case=False)]['id'].to_string(index=False)
        return clinic_id
    except:
        return "Cannot find selected clinic"
    

def date_selector(clinic_id):
    """Must input clinic id as parameter. Displays clinic's operation hours. Returns date in %Y-%m-%d, start_time and end_time."""

    df = pd.read_csv("chatbot\langsql\converted_functions\dentist_rand_sched_utf.csv")
    
    # select date of appointment
    date_today = datetime.now()
    # user_selected = "12/24/2023"
    # # accepts mm/dd/yyyy format only for now, use date picker if available
    date_format = '%m/%d/%Y'

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    print("Operating hours:")
    for day in days:
        time_start = df.loc[df['id'] == int(clinic_id)][f'{day}_start'].values
        if time_start >= 0:
            time_end = df.loc[df['id'] == int(clinic_id)][f'{day}_end'].values
            print(f"{day} | {int(time_start[0])}:00 - {int(time_end[0])}:00")

    while True:
        user_selected = input("Please type desired date in mm/dd/yyyy format.\n")
        # check if date is done or not
        try:
            user_date = datetime.strptime(user_selected, date_format)
            if user_date < date_today:
                print("cant select that date") # change error message para maganda
            else:
                # check if selected clinic can accomodate that day
                sch_day = user_date.strftime('%A')
                time_start = df.loc[df['id'] == int(clinic_id)][f'{sch_day}_start'].values
                
                can_accomodate = time_start[0]>0
                
                if can_accomodate:
                    return user_date.date()
                else:
                    print("cant select that date")
        except:
            if user_selected.lower() == 'q':
                break
            else:
                print("Not a date bro") # Change message here


def time_selector(date, clinic_id):
    df = pd.read_csv("chatbot\langsql\converted_functions\dentist_rand_sched_utf.csv")
    day = date.strftime('%A')
    time_start = df.loc[df['id'] == int(clinic_id)][f'{day}_start'].values
    # 4845 CORREA 10-11
    while True:
        user_time = input("Type desired time. Use 24 hr format and omit the :00\n")
        try:
            user_time = int(user_time)
            if user_time >= time_start:
                # connect to db to check if time is taken
                sql_query = f"""SELECT COUNT(*) FROM app_dentist_schedule WHERE clinic_id = {clinic_id} AND appointment_date = '{date.strftime('%Y-%m-%d')}' AND "start" = {int(user_time)};"""
 
                conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=password)
                cur = conn.cursor()
                cur.execute(sql_query)
                ans = cur.fetchall()

                # add 1 to count 
                num = int(ans[0][0])
                if num > 0:
                    print("Selected time is taken")
                else:
                    return user_time
            elif int(user_time) < time_start:
                print(f'Operating hours on {day}s starts at {int(time_start[0])}:00')
        except:
            print("Please type in integer only.")


def generate_ctrl_num(date):
    """Accepts date and returns a control number. Add 1 to the int part of the control number if existing in DB."""

    # sample = QCYYYYMMDD001, QC20231203001
    date_part = date.strftime("%Y%m%d")

    # check db if how many control number on a certain date
    sql_query = f"SELECT COUNT(*) FROM app_dentist_schedule WHERE reference_number ILIKE '%QC{date_part}%';"
    conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=password)
    cur = conn.cursor()
    cur.execute(sql_query)
    ans = cur.fetchall()
    print(ans)

    # add 1 to count 
    num = int(ans[0][0]) + 1
    num_part = str(num).rjust(3, "0")
    return f'QC{date_part}{num_part}'

    

#set_appointment()
# NEED TO ADD CHECKER FOR TIME