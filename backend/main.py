from os import urandom
from flask import (
    Flask, abort, redirect
)
from flask_restful import (
    Api, Resource, reqparse
)
from flaskext.mysql import MySQL

app = Flask(__name__)
api = Api(app)

# session cookie management
app.config.update(
    session_cookie_secure=True,
    session_cookie_httponly=True,
    session_cookie_samesite='****'
)

# mysql cfg
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = ''  # Database username
app.config['MYSQL_DATABASE_PASSWORD'] = ''  # Database password
app.config['MYSQL_DATABASE_DB'] = ''  # Database table name
app.config['MYSQL_DATABASE_HOST'] = ''  # Database hosts name
app.config['MYSQL_DATABASE_PORT'] = 0  # Database port
mysql.init_app(app)


# Receive client's data


class ParseRankData(Resource):
    def post(self):
        try:
            data = reqparse.RequestParser()
            data.add_argument('uid', type=str)
            data.add_argument('data', type=int)
            args = data.parse_args()

            uid = args['uid']
            parsed_data = args['data']

            connection = mysql.connect()
            cursor = connection.cursor()
            cmd = "INSERT INTO user_log VALUES(%s, %s, NOW());"

            cursor.execute(cmd, (uid, parsed_data))
            connection.commit()
            result = cursor.fetchall()

            if len(result) == 0:
                return {'StatusCode': 200, 'Message': 'Successfully Generated.'}
            else:
                return {'StatusCode': 200, 'Message': 'failed to generate data sets.'}

        except Exception:
            return {'error': 'Please Check Your Data sets again.'}


# client's data request
class RequestRankData(Resource):
    def post(self):
        try:
            data = reqparse.RequestParser()
            data.add_argument('uid', type=str)
            args = data.parse_args()

            uid = args['uid']

            conn = mysql.connect()
            cursor = conn.cursor()

            cmd = "SELECT data FROM user_log WHERE uid = %s ORDER BY data DESC limit 0, 5;"
            cursor.execute(cmd, (uid, cursor.rowcount))

            data = cursor.fetchall()
            result = data

            return {'StatusCode': 200, 'Message': result}

        except Exception as e:
            abort(401, "Invalid Contents.")


# error handler
@app.errorhandler(404)
def internal_error():
    return redirect("http://goerica.hanyang.ac.kr/")


api.add_resource(ParseRankData, '/user/v1/data')
api.add_resource(RequestRankData, '/user/v1/info')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
