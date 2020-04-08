from flask import Flask,make_response,request,jsonify,session
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

# Server Handler
"""
    The handler handles both GET and POST requests, fetches
    the data if a post request is sent as expected and uses,
    the student data from the payload it receives and returns the 
    corresponding sgpa of the student.
"""
@app.route('/gpacalc',methods=['GET','POST'])
def gpacalc():
    if request.method == 'POST':
        data = request.get_json()
        scores = [i["score"] for i in data]
        units = [i["units"] for i in data]
        total_grade = 0
        total_grade_point = 0
        total_units = sum(units)
        for i in data:
            if i["score"] in range(70,101):
                total_grade += 5
                total_grade_point += 5 * i["units"]
            elif i["score"] in range(60,70):
                total_grade += 4
                total_grade_point += 4 * i["units"]
            elif i["score"] in range(50,60):
                total_grade += 3
                total_grade_point += 3 * i["units"]
            elif i["score"] in range(45,51):
                total_grade += 2
                total_grade_point += 2 * i["units"]
            elif i["score"] in range(40,45):
                total_grade += 1
                total_grade_point += 1 * i["units"]
        session['sgpa'] = round(float(total_grade_point/total_units),2)
        return make_response("Added Data Successfully",200)
    else:
        sgpa = session['sgpa']
        return make_response(jsonify({"sgpa":sgpa}))

if __name__ == "__main__":
    app.run()
