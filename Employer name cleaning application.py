import pandas as pd
import difflib as dl
import csv
import sqlite3


# # Function definitions

def fetch_names(cursor):
    cursor.execute("SELECT * FROM employer_pairs")
    results = cursor.fetchall()
    pairs = {x[0]:x[1] for x in results}
    clean_employer_names = [str(x) for x in set(pairs.values())]
    clean_employer_names_for_compare = []
    employer_lookup = {x:y for x,y in pairs.items() if x!=y}
    dirty_employer_names = [str(x) for x in employer_lookup.keys()]
    return clean_employer_names, employer_lookup, dirty_employer_names


def match_name(name):
    global c # sqlite cursor
    clean_employer_names, employer_lookup, dirty_employer_names = fetch_names(c)
    if name in clean_employer_names:
        return name
    elif name in employer_lookup.keys():
        return employer_lookup[name]
    choices = dl.get_close_matches(name,clean_employer_names)
    choices2 = dl.get_close_matches(name,dirty_employer_names)
    choices2 = [employer_lookup.get(x) for x in choices2]
    reversed_choices = dl.get_close_matches(" ".join(list(reversed(name.split(" ")))),clean_employer_names)
    reversed_choices2 = [employer_lookup.get(x) for x in dl.get_close_matches(" ".join(list(reversed(name.split(" ")))),dirty_employer_names)]
    all_choices = choices + choices2 + reversed_choices + reversed_choices2
    all_choices = list(set(all_choices))
    if len(all_choices) == 0:
        user_name = input('Original: {}\nNo suggestions, please enter name or hit enter to use raw name:'.format(name))
        if user_name == '':
            c.execute("INSERT INTO employer_pairs (RAW_NAME, CLEAN_NAME) VALUES (?,?)",(name,name))
            clean_employer_names, employer_lookup, dirty_employer_names = fetch_names(c)
            return name
        c.execute("INSERT INTO employer_pairs (RAW_NAME, CLEAN_NAME) VALUES (?,?)",(name,user_name))
        clean_employer_names, employer_lookup, dirty_employer_names = fetch_names(c)
        return user_name
    else:
        choice_string = ''.join(["\n{}){{}}".format(i+1) for i in range(len(all_choices))])
        choice_string = "Original: {}\nChoices:" + choice_string + "\n99)Keep original name\nOr just type a revised name\n"
        choice_num = input(choice_string.format(name,*all_choices))
        try:
            val = int(choice_num)
            if val != 99:
                fixed_name = all_choices[int(choice_num)-1]
                c.execute("INSERT INTO employer_pairs (RAW_NAME, CLEAN_NAME) VALUES (?,?)",(name,fixed_name))
                clean_employer_names, employer_lookup, dirty_employer_names = fetch_names(c)
                return fixed_name 
            else:
                c.execute("INSERT INTO employer_pairs (RAW_NAME, CLEAN_NAME) VALUES (?,?)",(name,name))
                clean_employer_names, employer_lookup, dirty_employer_names = fetch_names(c)
                return name
        except ValueError:  
            c.execute("INSERT INTO employer_pairs (RAW_NAME, CLEAN_NAME) VALUES (?,?)",(name,choice_num))
            clean_employer_names, employer_lookup, dirty_employer_names = fetch_names(c)
            return choice_num


def process_raw_names(input_file_name,output_file_name):
    '''takes an Excel and runs it through the name cleaner
     with interaction from user
     input_file_name: string, path of Excel file with single column, Employer
     output_file_name: string, path of csv file with two columns old employer and standardized employer'''
    global c
    global conn
    raw_employers = pd.read_excel(input_file_name)
    raw_employers_list = list(raw_employers.Employer.values)
    employers_matched = {k:None for k in raw_employers_list}
    for n in raw_employers_list:
        if employers_matched[n] is None or employers_matched[n] == '':
            #print(n)
            employers_matched[n] = match_name(n)
            conn.commit()
    fout = open(output_file_name,"w")
    writer = csv.DictWriter(fout, ["old_name","standardized_name"])
    writer.writeheader()
    writeable_dict = [{"old_name":k, "standardized_name":v} for k,v in employers_matched.items()]
    for entry in writeable_dict:
        writer.writerow(entry)
    c.close()


# # Connect to database

conn = sqlite3.connect("employer_names.db")
c = conn.cursor()


#Test looking something up from database
c.execute("SELECT * from employer_pairs where CLEAN_NAME like '%Adobe%'")
c.fetchall()

#name the input and output files
input_file = "foo.xlsx"
output_file = "foo_cleaned.csv"

#run the application
process_raw_names(input_file, output_file)

