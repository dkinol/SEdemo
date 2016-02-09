from flask import Flask, render_template

from extensions import mysql
import controllers
import os

# Construct a Flask app instance
app = Flask(__name__, template_folder='templates')

#Creates our SQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'project2_485'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql.init_app(app)

app.secret_key = "mW\xba\xed>C\xb3N8'\x1eC\xe7\xd7\xa0i\x02\x1e,\xf0|\xb4\xc8b"

# Register Controllers file
app.register_blueprint(controllers.index)
app.register_blueprint(controllers.album)
app.register_blueprint(controllers.albums)
app.register_blueprint(controllers.user)

# Start server
if __name__ == '__main__':
	app.secret_key = "mW\xba\xed>C\xb3N8'\x1eC\xe7\xd7\xa0i\x02\x1e,\xf0|\xb4\xc8b"
	app.run(host='0.0.0.0', port=3000, debug=True)
