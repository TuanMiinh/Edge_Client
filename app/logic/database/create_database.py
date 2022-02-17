import sqlite3
import os

def final_create_db(database_path_):
    if os.path.exists(database_path_):
        os.remove(database_path_)
    conn_cre = sqlite3.connect(database_path_)
    c_cre = conn_cre.cursor()

    #Create tables
    c_cre.execute('''CREATE TABLE USERS(
                     [uuid] TEXT PRIMARY KEY,
                     [name] TEXT DEFAULT NAN,
                     [feature_vector] TEXT NOT NULL,
                     [avatar_url] TEXT NOT NULL) ''')
    conn_cre.commit()

    print("DB - INFO - Database created successfully")


final_create_db("AKACAM.db")

