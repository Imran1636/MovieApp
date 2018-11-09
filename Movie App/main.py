from flask import Flask,render_template,request,redirect
import sqlite3
import requests

connect = sqlite3.connect('movie.db',check_same_thread=False)
cursor = connect.cursor()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Home.html',title="DBMS Project")


@app.route('/add', methods=["GET","POST"])
def add():
    if request.method == "POST":
        form = request.form
        name = form["name"]
        email = form["email"]
        phone = form["phone"]
        cursor.execute("INSERT INTO USERS(name,email,phone) VALUES(?,?,?)",(name,email,phone))
        connect.commit()
        #return "Name: "+name+"<br>Email: "+email+"<br>Phone: "+phone
    return render_template('add.html',title="DBMS Project")


@app.route('/<name>/add_review',methods=["GET","POST"])
def add_blog(name):
    if request.method == "POST":
        form = request.form
        movie = form["movie"]
        movie = movie.title()
        rating = form["rating"]
        comment = form["comment"]
        cursor.execute("INSERT INTO movie_review(movie,rating,comments) VALUES(?,?,?)",(movie,rating,comment))
        connect.commit()
        red_page = name+"/home"
        return redirect(red_page)
    return render_template('add_review.html',title="DBMS Project",name=name)


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        form = request.form
        name = form["name"]
        phone = form["phone"]
        cursor.execute('SELECT * from USERS')
        a=cursor.fetchall()
        for i in a:
            if i[0]==name and i[2]==int(phone):
                return redirect('/'+name+'/home')
    return render_template('login.html',title="DBMS Project")


@app.route('/<name>/home')
def login_home(name):
    cursor.execute("SELECT * from USERS")
    a = cursor.fetchall()
    for i in a:
        if i[0]==name:
            phone = i[2]
            username = i[1]
    return render_template('user_home.html',title="Welcome",name=name,username=username,phone=phone)


@app.route('/<name>/search',methods=["GET","POST"])
def movie_search(name):
    if request.method == "POST":
        form = request.form
        url = "https://api.themoviedb.org/3/search/movie?api_key=c2a1f35ee881cedae3683da1652dc943&query="
        movie = form["movie"]
        url = url+movie
        json_data = requests.get(url).json()
        id = json_data["results"][0]["id"]

        ## Casts ...
        cast_url = "http://api.themoviedb.org/3/movie/"+str(id)+"/casts?api_key=c2a1f35ee881cedae3683da1652dc943"
        json_character_data = requests.get(cast_url).json()
        chars = []
        for i in range(0,5):
            chars.append(json_character_data["cast"][i]["name"])

        ## Poster ..
        poster_url = "http://api.themoviedb.org/3/movie/"+str(id)+"/images?api_key=c2a1f35ee881cedae3683da1652dc943"
        json_poster_image = requests.get(poster_url).json()

        name = json_data["results"][0]["title"]
        rating = json_data["results"][0]["vote_average"]
        summary = json_data["results"][0]["overview"]
        date = json_data["results"][0]["release_date"]
        image = json_poster_image["backdrops"][0]["file_path"]

        cursor.execute('SELECT * from movie_review')
        a = cursor.fetchall()
        comm = []
        for i in a:
            if i[0]==name:
                comm.append(i[2])


        return render_template("results.html",summary=summary,rating=rating,date=date,title=name,chars=chars,image=image,comm=comm)
    return render_template('search.html')


if "__main__" == __name__:
    app.run(host="0.0.0.0")
