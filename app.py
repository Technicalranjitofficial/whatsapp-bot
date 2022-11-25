from  flask import  Flask,request
from datetime import datetime
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
cluster = MongoClient("cluster_url")
db = cluster["bakery"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)


@app.route("/",methods=["get","post"])
def reply():
    res = MessagingResponse()
    text = request.form.get("Body")
    number = request.form.get("From")
    user =users.find_one({"number":number})
    order = orders.find_one({"number":number})
    if bool(user) == False:
        res.message("Thanks for contacting *Technical Ranjit* \n\n"
                         "1️⃣ To *Contact* us \n 2️⃣ To *Select* your order" )

        users.insert_one({"number":number,"status":"main","message":[]})
    elif user["status"]=="main":
        try:
            option = int(text)
        except:
            res.message("Please Enter the Valid Response")
            return str(res)
        if option == 1:
            res.message("You can contact us through number : +9779826... \n email : technicalranjit@gmail.com")

        if option ==2:
            res.message("You have Selected Order Option")
            users.update_one({"number":number},{"$set":{"status":"ordering"}})
            res.message("You can select your order \n\n 1) option 1 \n 2) option 2")


        if option == 3:
            res.message("Thanks for Contacting")
            users.update_one({"number":number},{"$set":{"status":"main"}})
            return str(res)
    elif user["status"] == "ordering":
        res.message("Ordering block")
        try:
            op = int(text)
        except:
            res.message("Please Enter the Valid resposes ")
            return str(res)
        if op == 1:
            res.message("selected")
            if bool(order) == False:
                orders.insert_one({"number": number, "status": "ordered","orders":[{"item":text,"date":datetime.now()}]})
            else:
                orders.update_one({"number": number}, {"$push": {"orders":{ "item":text, "date": datetime.now()}}})

            users.delete_one({"number": number})

            res.message("You have selecteds order 1 \n Thanks for contacting your order will be delivered in 1 hr")
            return str(res)
    else:

        users.update_one({"number":number},{"$push":{"message":{"text":text,"date":datetime.now()}}})
    return str(res)
if __name__ == "__main__":
    app.run()
