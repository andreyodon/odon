from website import create_app
from flask_mysqldb import MySQL

app = create_app()
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "util_artefakt"
app.config['MYSQL_PASSWORD'] = "artefakt"
app.config['MYSQL_DB'] = "artefakt_ai"

mysql = MySQL(app)


if __name__ == '__main__':
    app.run(debug=True)
