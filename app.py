from flask import Flask, render_template,request,redirect,url_for
from bson import ObjectId
from pymongo import MongoClient
import webbrowser

app = Flask(__name__)

'''Mongo DB Configs'''
#app.config["MONGO_URI"] = "mongodb://localhost:27017/SomeDatabase"
#app.config['MONGO_DBNAME'] = 'SomeCollection'
#app.config['SECRET_KEY'] = 'secret_key'
title = "todolist"   
client = MongoClient("mongodb://127.0.0.1:27017") #local host url 
db = client.todolist   #Select the database  
todos = db.todolist

'''Telegram Configs'''
token = '822016664:AAHGbmUBbSyJXvnMEHVbw8MAQB6Us8kZpCw'
chat_id = '372601813'
url = "https://api.telegram.org/bot"+token

def getMe():
    response = webbrowser.open(url+"/getMe")
    #print(response)

@app.route("/")
def index():
    completed_l = todos.find({"done":"yes"}).sort([("due_date", 1)]) #ascending order
    numcomplete = todos.find({"done":"no"}).count()
    incompleted_l = todos.find({"done":"no"}).sort([("due_date", 1)])
    return render_template("index.html", complete=completed_l, incomplete=incompleted_l, numcomplete=numcomplete, t=title)


#Adding tasks redirect
@app.route("/addtask", methods=["GET","POST"])  
def addtask():  
    #Adding a Task  
    print("reached")
    if request.method == "POST":
        duedate=request.form.get("Duedate")  
        task=request.form.get("task")   
        todos.insert({"due_date":duedate, "task":task, "done":"no"})  
        return redirect(url_for("index")) 



#Adding tasks redirect
@app.route("/removetask", methods=["GET","POST"])  
def removetask():  
    #Adding a Task  
    print("reached remove")
    if request.method == "POST":
        key=request.form.get("checks")
        print(key)
        todos.update({"_id":ObjectId(key)},{"$set": {"done":"yes"}})  
        return redirect(url_for("index")) 

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


if __name__ == "__main__":
    app.run(debug=True)