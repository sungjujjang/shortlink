from flask import Flask, render_template, url_for, redirect, request
import string
import random
import datetime
import sqlite3

app = Flask(__name__)

main_url = "http://linkshort.kro.kr:1111"

def randomstrings():
    letters_set = string.ascii_letters
    random_list = random.sample(letters_set, 10)
    result = ''.join(random_list)
    return result

def checkstring(string):
    con = sqlite3.connect('./links.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM Msg WHERE newlink = ?', (string,))
    data = cur.fetchone()
    con.close()
    if data:
        return data
    else:
        return None

def is_valid_url(url):
    return url.startswith('http://') or url.startswith('https://')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<randomstring>')
def urli(randomstring):
    link = checkstring(randomstring)
    if link:
        return redirect(link[0])
    else:
        return render_template('index.html')

@app.route('/create')
def create():
    link = request.args.get('link')
    if is_valid_url(link) == False:
        return "링크는 http:// 또는 https://로 시작하여야 합니다."
    randomstringst = randomstrings()
    now = datetime.datetime.now()
    con = sqlite3.connect('./links.db')
    cur = con.cursor()
    cur.execute('INSERT INTO Msg VALUES(?, ?, ?);', (link, randomstringst, now))
    con.commit()
    con.close()
    return main_url + f"/{randomstringst}"


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=1111)