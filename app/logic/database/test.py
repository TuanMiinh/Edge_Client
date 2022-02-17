import os

import requests

import run_model_service
import database_untils
import cv2
import sqlite3

database_path = 'AKACAM.db'
data_temp_users = './USER'
data = []
image_path = 'FACE_IMAGE'
list_img = os.listdir(image_path)

for img in list_img:
    path_img = os.path.join(image_path, img)
    img_to_cv = cv2.imread(path_img)
    img_resize = cv2.resize(img_to_cv, (200, 200))
    to_vector = img_resize.flatten()
    data.append(to_vector)
#../logic/database/FACE_IMAGE/1.jpg
# regis_returned_data = {
#     "name": "Pham Nhat Huy",
#     "avatar": "../logic/database/FACE_IMAGE/3.jpg"
# }
# run_model_service.regis_new_user("150", data[2], regis_returned_data)

# conn = sqlite3.connect(database_path)
# c = conn.cursor()
# c.execute("SELECT * FROM USERS")
# rows = c.fetchall()
# for row in rows:
#     print(row)

# run_model_service.delete_user('DE148')
# a = database_untils.query_all_vectors_for_matching(conn,c)

# a = run_model_service.matching_user()
# print(a)


# a = requests.get('http://127.0.0.1:5000/').json()["name"]
# print(a)

# a = run_model_service.checking_uuid_in_db("DE148")
# print(a)
