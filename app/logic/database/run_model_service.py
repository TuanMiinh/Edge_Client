import random
import sqlite3

import numpy as np

from app.logic.database import database_untils

database_path = 'AKACAM.db'


def regis_new_user(uuid_, regis_feature_vector, regis_returned_data):
    conn = sqlite3.connect(database_path)

    data = {
        "key": uuid_,
        "status": "",
        "return": "",
        "message": ""
    }

    if regis_feature_vector is None:
        data["status"] = "ng"
        data["message"] = "User already exist on the system"
    elif len(regis_feature_vector) == 0 or any(elem is None for elem in regis_feature_vector):
        data["status"] = "ng"
        data["message"] = "Can not detect face"
    else:
        # insert uuid data to DB
        uuid_data = database_untils.get_uuid_data_form(uuid_, regis_returned_data["name"], regis_feature_vector,
                                                       regis_returned_data["avatar"])
        database_untils.insert_db(conn, uuid_data, "USERS")

        data["status"] = "ok"
        data["message"] = "User register successful"

    print(data["message"])


def delete_user(uuid_):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    database_untils.delete_by_uuid(conn, c, uuid_)


def matching_user():
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # image_org = cv2.imread(image_path_)
    # image_org_resize = cv2.resize(image_org, (200, 200))
    # image_org_to_vector = image_org_resize.flatten()

    query_result = database_untils.query_all_user_infor(conn, c)
    compare_uuid_list = [query_result[i][0] for i in range(len(query_result))]
    compare_name_list = [query_result[i][1] for i in range(len(query_result))]
    compare_encodings_list = [np.frombuffer(query_result[i][2]) for i in range(len(query_result))]

    # print("image_org_to_vector" + image_org_to_vector)

    result_random = random.randint(0, len(query_result) - 1)
    return {
        "uuid": compare_uuid_list[result_random],
        "name": compare_name_list[result_random],
        # "feature_vector": np.float64(compare_encodings_list[result_random]).tostring()
    }


def checking_uuid_in_db(uuid_):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    query_result = database_untils.query_all_user_infor(conn, c)
    uuid_list = [query_result[i][0] for i in range(len(query_result))]
    for i in range(len(uuid_list)):
        if uuid_ == uuid_list[i]:
            return {
                "status": "Found",
                "uuid": query_result[i][0],
                "name": query_result[i][1],
                "avatar_url": query_result[i][3]
            }
    return {
        'status': "Not Found"

    }
