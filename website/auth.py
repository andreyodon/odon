import MySQLdb.cursors
from website import create_app
from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from flask_mysqldb import MySQL
import bcrypt
import cv2
import os
from werkzeug.exceptions import abort

nomImOr = ""
nomImMod = ""

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

auth = Blueprint('auth', __name__)

app = create_app()

mysql = MySQL(app)


def get_post(post_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    new_post = cur.fetchone()
    print(new_post)
    cur.close()
    if post is None:
        abort(404)
    return post


def get_customer_id(email):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM Customer WHERE email=%s", (email,))
    user = cur.fetchone()
    customer_id = user['id']
    cur.close()
    if customer_id is None:
        abort(404)
    return customer_id


def process_img(img):
    imgmod = img
    imgmod[imgmod < 128] = 0
    return imgmod


@auth.route('/delete')
def delete_img():
    target = os.path.join(APP_ROOT, 'static')
    destination = "\\".join([target, nomImOr])
    destination_modif = "\\".join([target, nomImMod])
    os.remove(destination)
    os.remove(destination_modif)
    return render_template('upload.html', nomimageOr=nomImOr, nomimagemodif=nomImMod)


@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Customer WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if user is None:
            return render_template("sign_in.html", error="Incorrect E-mail !")
        else:
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['first_name'] = user['first_name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return render_template("sign_in.html", error="Incorrect password !")
    else:
        return render_template("sign_in.html")


@auth.route('/sign_out')
def sign_out():
    session.clear()
    return render_template("home.html")


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM gender"
    cursor.execute(query)
    gender = cursor.fetchall()
    query = "SELECT * FROM specialization"
    cursor.execute(query)
    specialization = cursor.fetchall()
    query = "SELECT * FROM organization_type"
    cursor.execute(query)
    organization_type = cursor.fetchall()
    query = "SELECT * FROM pm_system"
    cursor.execute(query)
    pm_system = cursor.fetchall()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        organization = request.form['organization']
        specialization = request.form['specialization']
        organization_type = request.form['organization_type']
        pm_system = request.form['pm_system']

        hashed = bcrypt.hashpw(password, bcrypt.gensalt(12))

        params = [email]

        cur = mysql.connection.cursor()

        count = cur.execute("SELECT * FROM customer WHERE email=%s", (params))

        if count == 0:
            cur.execute(
                "INSERT INTO Customer (first_name, last_name, gender_id, email, password, organization, specialization_id, organization_type_id, pm_system_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (first_name, last_name, gender, email, hashed, organization, specialization, organization_type,pm_system,))

            mysql.connection.commit()
            session['first_name'] = first_name
            session['email'] = email

            return redirect(url_for("views.home"))

        else:
            query = "SELECT * FROM gender"
            cursor.execute(query)
            gender = cursor.fetchall()
            query = "SELECT * FROM specialization"
            cursor.execute(query)
            specialization = cursor.fetchall()
            query = "SELECT * FROM organization_type"
            cursor.execute(query)
            organization_type = cursor.fetchall()
            query = "SELECT * FROM pm_system"
            cursor.execute(query)
            pm_system = cursor.fetchall()
            return render_template("sign_up.html", error="E-mail already exist !", gender=gender, specialization=specialization, organization_type=organization_type, pm_system=pm_system)

    return render_template("sign_up.html", gender=gender, specialization=specialization, organization_type=organization_type, pm_system=pm_system)


@auth.route('/post')
def index():
    customer_id = get_customer_id(session['email'])
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM posts WHERE Customer_id = %s', (customer_id,))
    posts = cur.fetchall()
    cur.close()
    print(posts)
    return render_template('FlaskBlog.html', posts=posts)


@auth.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@auth.route('/upload')
def upload():
    return render_template('upload.html')


@auth.route('/traitement')
def traitement():
    target = os.path.join(APP_ROOT, 'static')
    destination = "\\".join([target, nomImOr])
    customer_id = get_customer_id(session['email'])
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('INSERT INTO x_ray (link, customer_id) VALUES ( %s, %s);', (destination, customer_id,))
    x_ray_id = cur.lastrowid
    destination_modif = "\\".join([target, nomImMod])
    cur.execute('INSERT INTO x_ray_segmentation (link, x_ray_id) VALUES ( %s, %s)', (destination_modif, x_ray_id,))
    mysql.connection.commit()
    cur.close()
    return render_template('traitement_image.html', nomimageOr=nomImOr, nomimagemodif=nomImMod)


@auth.route('/upload', methods=['GET', 'POST'])
def upload_file():
    target = os.path.join(APP_ROOT, 'static')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    if request.method == 'POST':
        # Récupération du nom du fichier :
        f = request.files['file']
        if f.filename == '':
            return render_template('upload.html', error="Choose a file before upload !")
        elif f.filename.split('.')[1] not in ALLOWED_EXTENSIONS:
            return render_template('upload.html', error="Extension not supported !")
        else:
            destination = "\\".join([target, f.filename])
            print("\n\t" + destination + "\n")
            f.save(destination)

            # Lecture de l'image :
            imageNG = cv2.imread(destination, 0)
            print(imageNG.shape)

            # Traitement de l'image :
            mod = process_img(imageNG)

            # Sauvegarde :
            var = os.path.splitext(f.filename)
            nomimagemodif = var[0] + "_modif" + var[1]
            print("mod : " + nomimagemodif)
            cv2.imwrite("website/static/" + nomimagemodif, mod)

            global nomImOr
            global nomImMod
            nomImOr = f.filename
            nomImMod = nomimagemodif

            # return 'file uploaded successfully'
            return render_template('affichage_image.html', nomimageOr=nomImOr, nomimagemodif=nomImMod)


@auth.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('INSERT INTO posts ( title, content, customer_id) VALUES ( %s, %s, %s)',
                         (title, content, get_customer_id(session['email'],)))
            cur.close()
            return redirect(url_for('auth.index'))

    return render_template('create.html')


@auth.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('UPDATE posts SET title = %s, content = %s WHERE id = %s',
                         (title, content, id))
            cur.commit()
            cur.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@auth.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('DELETE FROM posts WHERE id = %s', (id,))
    cur.commit()
    cur.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))