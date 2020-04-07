# Filename: day13.py

from flask import Flask,jsonify,request,make_response,session
import os

app = Flask(__name__)

# App's Config
"""
    The single-line clause beliow, configures the app, with a
    secret key that's required to encrypt data in session
    variables - It's bad practice to leave the secret key
    open - so to run app you'll be prompted to enter a key
    (anything you like) otherwise set it as an environment
    variable using the keyword 'SKEY'
"""
app.config['SECRET_KEY'] = f"{input('Enter a secret_key: ')}" or os.getenv("SKEY")

@app.route("/createdata",methods=['POST'])
def create():
    """
        The create() view accepts only POST requests as sepcified
        takes the sent payload and stores it in session.
        then retuns json of the stored data
    """
    data = request.get_json()
    session['data'] = data
    return make_response(jsonify({"payload":session['data']}),200)

@app.route('/getdata',methods=['GET'])
def get():
    """
        The get() view accepts only GET requests as sepcified
        then retuns json of the stored data
    """
    data = session['data']
    return make_response(jsonify({"payload":data}),200)

if __name__ == "__main__":
    app.run()