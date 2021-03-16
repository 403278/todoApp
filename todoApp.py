from flask import (
    Flask,
    g,
    redirect, 
    render_template, 
    url_for, request,
    make_response, 
    session,
    url_for,
    json
)
# from flask_material import Material
import appDB as db
import sqlite3 
# from appDB import db

app = Flask(__name__)
app.secret_key = 'Th!s-!s-$ecret'
# Material(app)

def get_db_connection():
    cur = None
    try:
        cur = sqlite3.connect('todoDB.db')
        cur.row_factory = sqlite3.Row
        return cur
    except sqlite3.Error as e:
        print(e)
    return cur


@app.route('/')
@app.route('/home', methods =['GET', 'POST'])
def home():
    print("you are in home end-point")
    if request.method == 'GET':
        print("this is GET home")
        if 'cname' in session:
            clientname = session['cname']
            print(clientname)
            # with sqlite3.connect("todoDB.db") as connection:
            cur = get_db_connection()
            posts = cur.execute("SELECT * FROM Activity WHERE clientname= ?;", (clientname,)).fetchall()
            # cur.execute("SELECT * FROM Activity WHERE clientname= ?;", (clientname,))
            # activity = [
            #     dict(clientname=row[0], chores=row[1], finished=row[2])
            #     for row in cur.fetchall()
            # ]
            # if activity is not None:
            #     return json.dumps(activity)
            return render_template('home.html', title='Home', cname = session['cname'], posts=posts)
        else:
            return render_template('login.html', title= 'Login')
    else:
        print("this is POST home")


@app.route('/chore', methods =['GET', 'POST'])
def chore():
    print("you are in chore end-point")
    if request.method == 'GET':
        print("this is GET chore")
        if 'cname' in session:
            clientname = session['cname']
            print(clientname)
            return render_template('chore.html', title='chore', cname = session['cname'])
        else:
            return render_template('login.html', title='Login')
    else:
        print("this is POST chore")

        clientname = session['cname']
        chores = request.form["chores"]
        finished = request.form["finished"]
        # querry the database to check for the activity 
        with sqlite3.connect("todoDB.db") as conn:
            # db.newActivity()
            cur = conn.cursor()
            cur.execute("INSERT INTO Activity VALUES (?, ?, ?);", (clientname, chores, finished))
            conn.commit()

        return render_template('home.html', title= 'Home', cname = session['cname'])


@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'GET':
        print("this is a GET request")
        return render_template('register.html', title = 'Register')
    else:
        print("this is a POST request")

        clientname = request.form["clientname"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        password = request.form["password"]
        # querry the database to check for the client 
        with sqlite3.connect("todoDB.db") as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO Client VALUES (?, ?, ?, ?);", (clientname, password, firstname, lastname))
            conn.commit()
            # conn.close()
        
        return render_template('login.html', title= 'Login')


@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'GET':
        print("this is a GET request")
        return render_template('login.html', title = 'Login')
    else:
        print("this is a POST request")
        clientname = request.form["cname"]
        password = request.form["password"]
        # check the provided password
        with sqlite3.connect("todoDB.db") as connection:
            cur = connection.cursor()
            cur.execute("SELECT * FROM Client WHERE clientname= ? AND password= ? ;", (clientname, password))
            row = cur.fetchone()
            if row:
                # sessions
                session['cname'] = clientname 
                print(session['cname'])
                if 'cname' not in session:
                    request.session['cname'] = 0
                    print(request.session['cname'])
                    return redirect(url_for('home'))
                
            return render_template('home.html', title='Home', cname= clientname)



        
@app.route('/logout')
def logout():
    # remove the clientname from the session if it's there
    session.pop('cname', None)
    return redirect(url_for('login'))        

if __name__ == '__main__':
    app.run(host="18.184.217.98",port=80)