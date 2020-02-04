from flask import Flask, render_template,request,redirect,url_for
from bson import ObjectId
from pymongo import MongoClient
import webbrowser

app = Flask(__name__)

'''Mongo DB Configs'''
title = "todolist"   
#Atlas database
pwd = "goGgY9rm3GOBrogi"
client = MongoClient("mongodb+srv://kkmongodb:"+pwd+"@cluster0-ixdqm.gcp.mongodb.net/test?retryWrites=true&w=majority")
#client = MongoClient("mongodb://127.0.0.1:27017") #local host url 
db = client.todolist #Select the database  
#todos = db['todolist']
todos = db.todolist

'''Telegram Configs'''
token = '822016664:AAHGbmUBbSyJXvnMEHVbw8MAQB6Us8kZpCw'
chat_id = '372601813'
url = "https://api.telegram.org/bot"+token

def getMe():
    response = webbrowser.open(url+"/getMe")
    #print(response)

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{}{}'.format(url, token))
    #check if worked
    if s:
        print("webhook setup ok") 
    else:
        print("webhook setup failed") 
'''
def sendtext(id,text):
    data = {
      method: "post",
      payload: {
         method: "sendMessage",
         chat_id: String(id),
         text: text,
         parse_mode: "Markdown" // add markdown formatting
         //reply_markup: JSON.stringify(keyBoard)
      }
    }
'''

'''Web app part'''
@app.route("/", methods=["GET","POST"])
def index():
    #count the initial number of completed tasks
    numcompleted = todos.find({"done":"yes"}).count()
    
    completed_l = todos.find({"done":"yes"}).sort([("due_date", -1)])
    #count number of incomplete tasks
    numincomplete = todos.find({"done":"no"}).count()
    incompleted_l = todos.find({"done":"no"}).sort([("due_date", 1)])
    print("ticks working")
    value = "show"
    if request.method == "POST":
        value = request.form.get("check")
        if value == "hide":
            value = "hide"
        else:
            value = "show"
    
    return render_template("index.html", hidevalue=value,complete=completed_l, incomplete=incompleted_l, numincomplete=numincomplete, t=title)


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

if __name__ == "__main__":
    app.run(debug=True)