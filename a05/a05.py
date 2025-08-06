from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route("/")
def item():
    a1=random.randint(1,10)
    return render_template('index.html', a1=a1)


if __name__ =="__main__":
    app.run()