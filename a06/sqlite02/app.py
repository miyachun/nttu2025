from flask import Flask, render_template, request, url_for, flash, redirect, abort
import sqlite3


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

def get_db_connection():
    conn = sqlite3.connect('mydb.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM COMPANY').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        ID = request.form['ID']
        NAME = request.form['NAME']
        AGE = request.form['AGE']
        ADDRESS = request.form['ADDRESS']
        SALARY = request.form['SALARY']

        if not ID:
            flash('Title is required!')
        elif not NAME :
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO COMPANY (ID, NAME, AGE, ADDRESS, SALARY ) VALUES (?, ?, ?, ?, ?)',
                         (ID, NAME, AGE, ADDRESS, SALARY ))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM COMPANY WHERE ID = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':

        
        NAME = request.form['NAME']
        AGE = request.form['AGE']
        ADDRESS = request.form['ADDRESS']
        SALARY = request.form['SALARY']
        if not NAME:
            flash('Title is required!')
        elif not AGE :
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE COMPANY SET NAME = ?, AGE = ?, ADDRESS = ?, SALARY = ?'
                         ' WHERE ID = ?',
                         ( NAME, AGE, ADDRESS, SALARY, id))

            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM COMPANY WHERE ID = ?', (id,))
    conn.commit()
    conn.close()
    flash('was successfully deleted!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
