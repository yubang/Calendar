#coding:UTF-8

from flask import Flask,render_template,request,redirect,session
from functools import wraps
from config import db
import time

app=Flask(__name__)
app.secret_key="root"

def checkUser(fn):
    @wraps(fn)
    def deal(*args,**kwds):
        if session.has_key("uid"):
            return fn(*args,**kwds)
        else:
            return redirect("/account")
    return deal

def handleListsCharset(obj):
    r=dict(obj.items())
    r['content']=r['content'].decode("UTF-8")
    if(r['endDate']==None):
        r['endDate']=u"无"
    return r


@app.route("/")
@checkUser
def index():
    "主页"
    dao=db.execute("select * from calendar where status = 0 order by level desc,endDate asc,id desc")
    lists=dao.fetchall()
    dao.close()
    lists=map(handleListsCharset,lists)
    return render_template("index.html",lists=lists)
    
    
@app.route("/add",methods=['GET','POST'])
@checkUser
def add():
    "添加日程"
    if request.method == "GET" :
        return render_template("add.html")
    else:
        level=request.form.get("level",None)
        content=request.form.get("content",None)
        endDate=request.form.get("endDate",None)
        dao=db.execute("insert into calendar(level,content,endDate,createTime) values('%s','%s','%s',now())"%(level,content,endDate))
        dao.close()
        return redirect("/")


@app.route("/account",methods=['GET','POST'])
def account():
    "用户登录"
    if request.method == "GET":
        code=request.args.get("code","3")
        return render_template("account.html",code=code)
    else:
        username=request.form.get("username",None)
        password=request.form.get("password",None)
        dao=db.execute("select password from account where username = '%s' limit 1"%(username))
        obj=dao.fetchone()
        dao.close()
        if obj == None:
            url="/account?code=1"
        elif obj.password == password:
            session['uid']=time.time()
            url="/"
        else:
            url="/account?code=2"
        return redirect(url)


@app.route("/finish")
def finish():
    "完成日程"
    id=request.args.get("id",None)
    dao=db.execute("update calendar set status = 1 where id = %s"%(id))
    dao.close()
    return redirect("/")        
        
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8000)
