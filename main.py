#New comment
from website import create_app
from flask_mysqldb import MySQL

app = create_app()
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "artefakt-ai"

mysql = MySQL(app)


if __name__ == '__main__':
    app.run(debug=True)
