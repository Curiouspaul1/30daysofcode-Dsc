# Filename: day13.py

from flask import Flask,jsonify,request,make_response,session
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SKEY")

@app.route("/createdata",methods=['POST'])
def create():
    data = request.get_json()
    session['data'] = data
    return make_response(jsonify({"payload":data}),200)

@app.route('/getdata',methods=['GET'])
def get():
    data = session['data']
    return make_response(jsonify({"payload":data}),200)

if __name__ == "__main__":
    app.run(debug=True)