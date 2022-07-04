import requests
import json
# from flask import Flask , jsonify ,request, render_template
import flask
from flask_restful import Resource, Api
import json
import urllib
# from urllib import urlopen
import pymysql
import pandas as pd
import datetime
from flask_cors import CORS
from flask_cors import cross_origin

app = flask.Flask(__name__)
# api = Api(app)
# data = []
CORS(app)

@app.route('/')
@cross_origin()
def welcome():
    return "Welcome"

# @app.route('/hello/', methods=['GET', 'POST'])
# def hello():
#     return jsonify({"name": "Hello World!"})

#request:
obj = { 
       "clientId" : "Cl12" ,
       "workloadId":"IBMxyz", 
       "type":"any", 
       "geofencing":False, 
       "domainName":"xyz", 
       "ipAddress":"1.2.3.4",
       "port":"3306", 
       "gpu":"4GB", 
       "minRam": "20GB" , 
       "maxRam": "30GB", 
       "minCpu": 1 ,
       "maxCpu": 2 
    }

#provision details:
pro = {
    "wId":"IBMx",
    "type":"any",
    "selectedDC" : "X",
    "time" : "xyz",
    "requestInfo" : {
       "clientId" : 12 ,
       "workloadId":"IBMxyz", 
       "type":"any", 
       "geofencing":False, 
       "domainName":"xyz", 
       "ipAddress":"1.2.3.4",
       "port":"3306", 
       "gpu":"4GB", 
       "minRam": "20GB" , 
       "maxRam": "30GB", 
       "minCpu": 1 ,
       "maxCpu": 2 
    }
}

df = pd.DataFrame(obj , index=[1])
df.to_csv ('requests.csv', index = False, header=True)

dff = pd.DataFrame(pro , index=[1])
dff.to_csv ('selection.csv', index = False, header=True)

@app.route('/request/', methods=['GET', 'POST'])
def request():
    return flask.jsonify(obj)

@app.route('/login', methods=["GET" , "POST"])
@cross_origin()
def login():
    if flask.request.method == "POST":
        # req = flask.request.form
        
        req = flask.request.get_json()
        obj["minRam"] = req["minRam"]
        obj["maxRam"] = req["maxRam"]
        obj["minCpu"] = req["minCpu"]
        obj["maxCpu"] = req["maxCpu"]
        obj["type"] = req["type"]
        obj["gpu"] = req["gpu"]
        
        url = 'http://ipinfo.io/json'
        response = urllib.request.urlopen(url)
        data = json.load(response)

        obj["ipAddress"]=data['ip']
        
        # res = requests.post('http://localhost:5000/getrequest', json=obj)
        newdf = pd.DataFrame(obj,index = [1])
        newdf.to_csv('requests.csv', mode='a', index=False, header=False) #append
        # return flask.jsonify(obj)
        return flask.redirect(flask.url_for("alloc", req=obj))
        # return flask.render_template("resp.html" , dc1 = "A" , dc2 = "B" , dc3 = "C" )
        # obj["dcChosen"] = "A"
        # return flask.render_template("resp.html" , dc1 = res.dc1 , dc2 = res.dc2 , dc3 = res.dc3 )
    else:
        response = flask.jsonify(message="Simple server is running")

        # Enable Access-Control-Allow-Origin
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
        # return flask.render_template("req.html")

@app.route('/alloc/<req>', methods=["GET" , "POST"])
def alloc(req):
    if flask.request.method == "POST":
        reqst = flask.request.form
        if(reqst["dcChosen"] != "none"):
            pro["selectedDC"] = reqst["dcChosen"]
            
            # pro["type"] = type
            # pro["wId"] = wId 
            pro["requestInfo"] = req
            pro["time"] = datetime.datetime.now()
            
            newdff = pd.DataFrame(pro,index = [1])
            newdff.to_csv('selection.csv', mode='a', index=False, header=False) #append
        
        return flask.jsonify(pro)
    else:
        response = flask.jsonify({ 'dc1': 'Greenwood' , 'dc2' : 'Dallas' , 'dc3':'Tokyo'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

        # return flask.render_template("resp.html" , dc1 = "GreenWood Data Center" ,cue1 = "172g", dc2 = "Dallas Data cente" , cue2="190g",cue3="200g", dc3 = "Tokyo Data cente" )

# url = 'http://ipinfo.io/json'
# response = urlopen(url)
# data = json.load(response)

# IP=data['ip']
    
# @app.route('/reply/', methods=['GET'])
# def request():
#     return flask.jsonify(obj)

if __name__ == '__main__':
    app.run(debug = True)
    # app.run(host='0.0.0.0', port=105)


# res = requests.post('http://localhost:5000/tests/endpoint', json = obj)
# # print res.text
# dictFromServer = res.json()



# post 
# url = 'https://www.w3schools.com/python/demopage.php'

# x = requests.post(url, data = myobj)

# obj = [{ “clientId” : 12 , “workloadId”:IBMxyz , “type”:"any", “geofencing”:false, “domainName”:"xyz", “ipAdress”:"1.2.3.4",”port”:xyz, “gpu”:xyz, “minRam”: “20GB”, "maxRam”: “30GB”, “minCpu”: 1 , “maxCpu”:2 }]


# obj = { 'clientId' : 12 , 'workloadId' :"IBMxyz" , 'type':"any", 'geofencing':false, 'domainName':"xyz", 'ipAdress' :"1.2.3.4",'port':xyz, 'gpu':xyz, 'minRam': “20GB”, 'maxRam': “30GB”, 'minCpu': 1 , 'maxCpu':2 }
# type: any/container/vm

# # To make a ‘GET’ request, we’ll use the requests.get() function, which requires one argument — the URL we want to make the request to
# response = requests.get("https://api.open-notify.org/this-api-doesnt-exist")

# # The get() function returns a response object. We can use the response.status_code attribute to receive the status code for our request:
# print(response.status_code)

# # to see the data we received back from the API:
# print(response.json())

# def sqlSave(obj):
#     cnx = pymysql.connect(host='localhost',port = 3306,user='root', password='mysql@ns20', db='client')
#     if(cnx):
#         print("Successfully connected to SQL")
#     cur = cnx.cursor()
#     cur.execute("SHOW DATABASES")
#     results=cur.fetchall()
#     for result in results:
#         print (result)
#     # cur.execute("USE client")
#     cur.execute("SHOW TABLES")
#     results=cur.fetchall()
#     for result in results:
#         print (result)
#     typ = obj["type"]
#     cur.execute("INSERT INTO request (type) VALUES (typ)")
        
#     cur.execute("SELECT * FROM request")
#     output = cur.fetchall()
#     print(output)

    # cnx.close()