from flask import Flask,jsonify,make_response,request

app = Flask(__name__)

# Native function
def palindromecheck(str):
    """
        palindromecheck is a fullproof palindrome detector 
        detects single word palindromes such as eve or 
        multiple word palindromes such as 'nurses run'\
        
        args: <class 'string'>
        returns: <class 'bool'>

        PS: this function is used in the server handler below to perdorm the
        check on received input from external applications
    """
    list1 = str.split(' ')
    if len(list1)==1:
        word = str[::-1]
        if word == str:
            return True
        else:
            return False
        pass
    else:
        placehold = []
        placehold1 = []
        for i in range(1,len(list1)+1):
            placehold.append(list1[-i])
        for i in placehold:
            placehold1.append(i[::-1])
        
        word = ''.join(i for i in placehold1)
        if word == ''.join(i for i in list1):
            return True
        else:
            return False

# Server Handler
@app.route('/drome',methods=['GET'])
def dromer():
    #data = request.get_json()
    words = request.get_json()['words']
    dict_ = []
    for word in words:
        if palindromecheck(word):
            dict_.append(word)
    return make_response(jsonify({"words":dict_}),200)


if __name__ == '__main__':
    app.run()