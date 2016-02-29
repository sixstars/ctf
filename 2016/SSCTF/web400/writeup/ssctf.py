# -*- coding: utf-8 -*-
from flask import Flask,abort,request,session,redirect,render_template_string
import os
import json
import datetime
import urllib
import re
import time
import hashlib
#import sqlite3
import threading
from rauth.service import OAuth2Service

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = os.name =='nt'
if DEBUG:
    WEBHOME = 'http://127.0.0.1/'
else:
    WEBHOME = 'http://b525ac59.seclover.com/'



github = OAuth2Service(
    name='github',
    base_url='https://api.github.com/',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    client_id= '6ad5ab3c971c740adf64',
    client_secret= 'd6aed929c3b9bf713a37435c117619dcd46194e1',
)






app = Flask(__name__)
app.debug = DEBUG
app.secret_key = "sflkgjsiotu2rjdskjfnpwq9rwrehnpqwd0i2ruruogh9723yrhbfnkdsjl"
app.flagman = (1,'flagman','SSCTF{dc28c39697058241d924be06462c2040}','http://www.seclover.com/wp-content/uploads/2015/07/logo.png')
# app.lastid = 1
# app.lock = threading.Lock()
# def getnewid():
#     app.lock.acquire()
#     app.lastid+=1
#     newid = app.lastid 
#     app.lock.release()
#     return newid

# def dbinsert(name,uid,pic):
#     newid = getnewid()
#     app.user[newid] = (name,uid,pic)
#     return newid
# def dbfind(user_id):
#     userinfo = app.user.get(user_id)
#     if userinfo:
#         return (user_id,)+userinfo
#     return None

# def dbfind_uid(uid):
#     for u in app.user:
#         if app.user[u][1]==uid:
#             return (u,)+app.user[u]
#     return None
# app.dbcon = sqlite3.connect(":memory:", check_same_thread=False)
# app.dbcur = app.dbcon.cursor()
# app.dbcur.executescript('''CREATE TABLE "user" (
# "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
# "name"  TEXT,
# "uid"  TEXT,
# "pic"  TEXT
# )
# ;

# CREATE UNIQUE INDEX "id"
# ON "user" ("id" ASC);

# CREATE UNIQUE INDEX "uid"
# ON "user" ("uid" ASC);

# ''')



# def dbinsert(name,uid,pic):
#     sql = '''INSERT INTO "user" ("name", "uid", "pic") VALUES (?,?,?);'''
#     app.dbcur.execute(sql,(name,uid,pic))
#     app.dbcon.commit()
#     return app.dbcur.lastrowid
# def dbfind(user_id):
#     sql = '''SELECT * FROM "user" where id = ?'''
#     rows = app.dbcur.execute(sql,(user_id,))
#     for id,name,realuid,pic in rows:
#         return (id,name,realuid,pic)
#     return None

# dbinsert('howmp','uid','http://www.seclover.com/wp-content/uploads/2015/07/logo.png')


@app.route('/user/')
def user():
    userinfo = session.get('info')
    if not userinfo:
        #session.pop('info')
        return "please <a href='/'>login</a> first.<br><b style='color: white;'>Powered by Flask/0.11.2</b>"
    user_id,name,realuid,pic = userinfo
    if user_id == 1:
        user_id,name,realuid,pic = app.flagman
    name = str(name)
    pic = str(pic)
    template = u'''<img src="{{pic}}" /><br><lable>name:''' + name + '</lable><br><lable>uid:{{ realuid }}</lable><br><lable>id:{{ user_id }}</lable>'
    #template += u"<br>{{app.secret_key}}"
    return render_template_string(template,**(dict(globals(), **locals())))


@app.route('/')
def index():
    def _link():
        params = {'redirect_uri': WEBHOME+'callback'}
        icon = u'<img src="https://developer.github.com/assets/images/status-icon-good.png" />'
        return """<div>
        <a href="%s">%s</a>
        </div>""" % (github.get_authorize_url(**params), icon)

    html = """<!DOCTYPE html>
    <html>
        <body>%slogin<br>only <code>/</code> and <code>/user</code>,no other pages!</body>
    </html>
    """ % _link()
    return html

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        abort(401)
    data = dict(code=request.args['code'],
            redirect_uri=WEBHOME+'callback',
            )
    try:
    	auth = github.get_auth_session(data=data)
    	me = auth.get('user').json()
    	session['info']=[2,me['name'],me['id'],me['avatar_url']]
    	return redirect('/user/')
    except Exception,e:
        return e
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)