from flask import Flask
import run_model_service
from flask import request
database_path = 'AKACAM.db'

app = Flask(__name__)


@app.route('/')
def matching_user():
    return run_model_service.matching_user()


@app.route('/get_user')
def get_user_info():
    uuid_ = request.args.get('uuid_')
    return run_model_service.checking_uuid_in_db(uuid_)


if __name__ == '__main__':
    app.run(port=6000)
