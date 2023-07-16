# coding=utf-8
from flask import Flask
# from flask import send_from_directory
from flask_cors import CORS
from flask import request
from flask import send_file
import pymysql
import random
import json
import time
# import requests
import uuid
import os
import math

"""
pip install flask
pip install flask_cors
pip install pymysql
"""

SEVER_STATUS = 0 # 0 is OK

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/', methods=['POST','GET'])
def test():
    messages = ['The server is running normally.',
            'Server development in progress.',
            'Server maintenance in progress.',
            'The server is not available.',
            'Server status unknown.']
    try:
        message = messages[SEVER_STATUS]
    except IndexError:
        message = messages[4]
    return {'status':SEVER_STATUS,
            'message':message, 
            'testid':uuid.uuid4()}

# Homepage recommendations
@app.route("/hp/com")
def com():
    posts = []
    con = pymysql.connect(
    host='localhost',
    user='YHjason',
    password='root',
    database='mhybbs',
    charset='utf8mb4'
)
    sql = f"SELECT * FROM posts"
    cur = con.cursor()
    cur.execute(sql)
    p = cur.fetchall()
    try:
        posts = [i[0] for i in random.sample(p, 4)]
    except ValueError:
        posts = [i[0] for i in p]
    
    return {"posts":posts} 

#Get Post of theme
@app.route('/hp/theme/<theme>',methods=['POST'])
def theme(theme):
    posts = []
    con = pymysql.connect(
    host='localhost',
    user='YHjason',
    password='root',
    database='mhybbs',
    charset='utf8mb4')
    cur = con.cursor()
    sql = f"SELECT id FROM posts where theme='{theme}'"
    try:
        cur.execute(sql)
        posts = [i[0] for i in cur.fetchall()]
    except:
        posts = []
    print(posts)
    # print(posts)
    con.close()
    
    return {"posts":posts}

#Post Infomation
@app.route("/post/<id>/content")
def post_content(id):
    status = 0
    con = pymysql.connect(
    host='localhost',
    user='YHjason',
    password='root',
    database='mhybbs',
    charset='utf8mb4'
)
    sqldata = []
    data = {}
    sql = f"SELECT * FROM posts WHERE id = '{id}'"
    cur = con.cursor()
    try:
        cur.execute(sql)    
        temp = cur.fetchone()
        if (temp is not None):
            sqldata = temp
        else:
            # status = 1
            return {'status':1}
    except:
        status = 1
    sqldata = list(sqldata)
    if (sqldata[4] == '0'):
        sqldata[4] = 'Robot'
    else:
        try:
            sql = f'select username from users where id="{sqldata[4]}"'
            cur.execute(sql)
            sqldata[4] = cur.fetchall()[0][0]
        except TypeError as e:
            status = 1
        except pymysql.Error as e:
            status = 1
    # print(sqldata[6])
    data = {"status":status,
            "title":sqldata[1], 
            "content":sqldata[2], 
            "likes":sqldata[3],
            "poster":sqldata[4],
            'theme':sqldata[5],
            'images':sqldata[6],
            'audio':sqldata[7]}
    return data
#Commit comment
@app.route("/post/<id>/comment/commit", methods=['POST'])
def commit(id):
    status = 0
    comment = request.get_data()
    comment = json.loads(comment)
    con = pymysql.connect(
    host='localhost',
    user='YHjason',
    password='root',
    database='mhybbs',
    charset='utf8mb4')
    sql = f'INSERT INTO comments (post_id, content,user_id) VALUES\
          (\"{id}\", \"{comment["content"]}\","{comment["uid"]}");'
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
    except pymysql.OperationalError:
        con.rollback()
        status = 1
    except:
        con.rollback()
        status = 1
    return {"status":status}
#Get comments
@app.route("/post/<id>/comment")
def comment(id):
    con = pymysql.connect(
    host='localhost',
    user='YHjason',
    password='root',
    database='mhybbs',
    charset='utf8mb4')
    sql = f'select * from comments where post_id="{id}"'
    cur = con.cursor()
    cur.execute(sql)
    data = list(cur.fetchall())
    data = [list(x) for x in data]
    for i,v in enumerate(data):
        sql = f'select username from users where id="{v[3]}"'
        cur.execute(sql)
        # print(v[3])
        uname = cur.fetchone()
        if uname is not None:
            data[i][3] = uname[0]
    if (not len(data)):
        # message = 'Invalid Request or No comment'
        cur.execute('select * from posts where id=%s', (id,))
        if (cur.fetchone() is None):
            message = 'Invalid Request'
        else:
            message = 'Successful'
    else:
        message = 'Successful'
    con.close()
    return {"comments":data,'message':message}
#Login
@app.route("/api/login", methods=['POST'])
def login():
    status = 0
    result = []
    con = pymysql.connect(
    host='localhost',
    user='YHjason',
    password='root',
    database='mhybbs',
    charset='utf8mb4')
    info = json.loads(request.get_data())
    uid = None
    sql = "SELECT * FROM users WHERE username=%s AND password=%s;"
    cur = con.cursor()
    try:
        cur.execute(sql, (info['username'],info['password']))
        result = cur.fetchall()[0]
        if (not result):
            status = 1
            return {'status':status}
        uid = result[0]
    except:
        status = 1
        con.rollback()
    finally:
        ...
    # create token
    token = uuid.uuid4()
    exp = time.time() + 172800
    sql = f'insert into tokens (token,exp,uid) values\
          ("{token}","{exp}","{uid}")'
    try:
        cur.execute(sql)
        con.commit()
    except:
        con.rollback()
    con.close()
    return {'status':status, 'uid':uid, 'token':token}
#Register
@app.route("/api/reg", methods=['POST'])
def reg():
    status = 0
    con = pymysql.connect(
    host='localhost',
    user='YHjason',
    password='root',
    database='mhybbs',
    charset='utf8mb4')
    info = json.loads(request.get_data())
    sql = "INSERT INTO users (username, password) VALUES \
        ('{}', '{}');".format(info['username'], info['password'])
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
    except pymysql.IntegrityError:
        con.rollback()
        status = 1
    finally:
        con.close()
    
    return {'status':status}

# @app.route('/api/user/uid/<uid>')
# def qu(uid):
#     con = pymysql.connect(
#     host='localhost',
#     user='YHjason',
#     password='root',
#     database='mhybbs',
#     charset='utf8mb4')
#     cur = con.cursor()
#     sql = f"select * from users where id=\"{uid}\""
#     cur.execute(sql)
#     info = cur.fetchone()
    
#     con.close()
#     return {'info':info}

#Get user infomation
@app.route('/api/user/token',methods=['POST'])
def token():
    con = pymysql.connect(
    host='localhost',
    user='YHjason',
    password='root',
    database='mhybbs',
    charset='utf8mb4')
    cur = con.cursor()
    uid = ()
    
    token = json.loads(request.get_data().decode('utf-8'))['token']
    sql = f'select exp from tokens where token="{token}"'
    cur.execute(sql)
    expdata = cur.fetchone()
    if (expdata != None):
        exp = expdata[0]
        if (float(exp) < time.time()):
            sql = f'delete from tokens where token="{token}"'
            try:
                cur.execute(sql)
                con.commit()
            except:
                con.rollback()
            con.close()
            return {'info':[],'exp':1}
    sql = f'select uid from tokens where token="{token}"'
    cur.execute(sql)
    uid = cur.fetchone()
    if (uid is not None):
        uid = uid[0]
    sql = f"select * from users where id=\"{uid}\""
    cur.execute(sql)
    info = cur.fetchone()
    if (info is None):
        info = []
    info = list(info)
    con.close()
    return {'info':info,'exp':0}

@app.route('/api/token/remove', methods=['POST'])
def remove_token():
    con = pymysql.connect(
    host='localhost',
    user='YHjason',
    password='root',
    database='mhybbs',
    charset='utf8mb4')
    cur = con.cursor()
    token = json.loads(request.get_data())['token']
    sql = f'delete from tokens where token="{token}"'
    try:
        cur.execute(sql)
        con.commit()
    except:
        con.rollback()
    con.close()
    return {}
#Likes post
@app.route('/post/<id>/like', methods=['POST'])
def like(id):
    status = 0
    uid = json.loads(request.get_data())['uid']
    con = pymysql.connect(
    host='localhost',
    user='YHjason',
    password='root',
    database='mhybbs',
    charset='utf8mb4')
    cur = con.cursor()
    try:
        sql = 'select poster from posts where id=%s'
        cur.execute(sql, (id,))
        poster = cur.fetchall()[0][0]
        # print(str(uid) == poster)
        if (str(uid) == poster):
            # status = 2
            return {'status':2}
        sql = 'INSERT INTO user_likes (user_id, post_id) VALUES \
            (%s, %s);'
        cur.execute(sql, (uid,id,))
        sql = 'UPDATE posts SET likes = likes + 1 where id=%s;'
        cur.execute(sql, (id,))
        sql = 'update users set mic = mic + 1 where id=%s'
        cur.execute(sql,(poster,))
        con.commit()
    except pymysql.err.IntegrityError as e:
        status = 1
        con.rollback()
    finally:
        con.close()
    return {'status':status}
#Create post
@app.route('/api/newpost',methods=['POST'])
def new_post():
    status = 0
    data = json.loads(request.get_data().decode('utf-8'))
    con = pymysql.connect(
    host='localhost',
    user='YHjason',
    password='root',
    database='mhybbs',
    charset='utf8mb4')
    cur = con.cursor()
    try:
        data['content'] = data['content'].replace("'",'\'').replace('"','\"')
        # print(data['content'])
        sql = f'INSERT INTO `mhybbs`.`posts` (title, content, poster, theme, images, audio) \
        VALUES (\'{data["title"]}\', %s,\'{data["uid"]}\',\
                  "{data["theme"]}","{data["images"]}", %s);'
        cur.execute(sql, (data['content'],data['audio'],),)
        con.commit()
    except pymysql.Error as e:
        status = 1
        print(e)
        con.rollback()
    finally:
        con.close()
    return {'status':status}

@app.route('/api/file/upload',methods=['POST'])
def image():
    img = request.files.get('file')
    status = 0
    # url = ''
    base = app.root_path
    filename = ''
    os.chdir(base)
    path = os.path.join(base,'static','imgs')
    if (not os.path.exists(path)):
        os.makedirs(os.path.join(path))
    if (img and img.filename):
        try:  
            imgbype = img.stream
            filename = str(math.floor(time.time())) + os.path.splitext(img.filename)[1]
            # print(os.path.splitext(img.filename)[1])
            with open(f'./static/' + filename
            , 'wb') as file:
                file.write(imgbype.read())
            img.close()
            # url = '/api/img/get/' + filename
        except Exception as e:
            print(e)
            status = 1
        finally:
            img.close()
    else:
        status = 2
    return {'status':status,'fn':filename}


# @app.route('/gacha',methods=['POST'])

@app.route('/api/file/get/<file>', methods=['POST','GET'])
def getImg(file):
    # print(file)
    try:
        return send_file(
            os.path.join(
            app.root_path,'static',file))
    except FileNotFoundError:
        return {'message':'Invalid Request'}

app.run(debug=True,host='0.0.0.0', port=5000
        )
        # ,ssl_context=('../cert.crt','../rsa_private.key'))
# ssl_context=('adhoc')