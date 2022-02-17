import numpy as np
import sqlite3
import pandas as pd


def insert_db(conn, data, table_name):
    try:
        data_form_add = pd.DataFrame.from_dict(data)
        print(data_form_add)
        data_form_add.to_sql(table_name, conn, if_exists="append", index=False)
        conn.commit()
        print("DB - INFO - Insert to DB(", table_name, ") successfully")
        return True
    except sqlite3.Error as error:
        print("DB - ERROR - Failed to insert data into ", table_name, " table bo: ", error)
        return False


def get_uuid_data_form(uuid_, name_, feature_vector,avatar_url):
    get_uuid_data_form = {
        "uuid": [uuid_],
        "name": [name_ if len(name_) > 0 else "NAN"],
        "feature_vector": [np.float64(feature_vector).tobytes()],
        "avatar_url":[avatar_url]
    }

    return get_uuid_data_form


def query_all_user_infor(conn, c):
    try:
        query_all_vectors = f"SELECT * FROM USERS"
        c.execute(query_all_vectors)
        return_all_feature_vector = c.fetchall()
        conn.commit()
        return return_all_feature_vector
    except sqlite3.Error as error:
        print("DB - ERROR - Failed to query all vectors for matching because of error: ", error)
        return None


def delete_by_uuid(conn, c, uuid_):
    try:
        delete_query = f"DELETE FROM USERS WHERE uuid = '{uuid_}'"
        c.execute(delete_query)
        conn.commit()
        print("DB - INFO - Delete uuid ", uuid_, " successfully")
    except sqlite3.Error as error:
        print("DB - INFO - Delete uuid ", uuid_, " bo error: ", error)
