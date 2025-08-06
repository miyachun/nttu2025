from flask import Flask, redirect, url_for, render_template, request, session
app = Flask(__name__)
app.secret_key = "#230dec61-fee8-4ef2-a791-36f9e680c9fc"
#login
@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        #user = request.form["nm"]
        #session["user"] = user
        userp = request.form["np"]
        session["userp"] = userp
        return redirect(url_for("user"))
    else:
        return render_template("login.html")

@app.route("/user")
def user():
    if "userp" in session:
        userp = session["userp"]
        if userp=='1234':
            return render_template("user.html",user=userp)
        else: 
            return render_template("user.html",user=userp)
    else:
        return redirect(url_for("login"))
if __name__ =="__main__":
    app.run()