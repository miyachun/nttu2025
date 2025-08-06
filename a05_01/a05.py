from flask import Flask, redirect, url_for, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "#230dec61-fee8-4ef2-a791-36f9e680c9fc"
a1=random.randint(1,10)
a2=random.randint(1,10)


@app.route("/", methods=["POST","GET"])
def item():
    global a1
    global a2

    if request.method == "POST":
        ans = request.form["ans"]
        session["ans"] = ans
        return redirect(url_for("ans"))
    else:
        return render_template("index.html",a1=a1,a2=a2)

    return render_template('index.html', a1=a1,a2=a2)


@app.route("/ans")
def ans():
    global a1
    global a2
    a3=a1+a2
    if "ans" in session:
        ans = int(session["ans"])
        print(type(ans))
        print(type(a3))
        if a3==ans:
            return render_template("ans.html",ok='答對')
        else: 
            return render_template('ans.html',ok='答錯')
    else:
        return render_template("ans.html")


if __name__ =="__main__":
    app.run()