from flask import Flask, request, render_template, Blueprint, jsonify
#from flask import Blueprint, request
from bson.json_util import dumps
from main2 import main
import os
app = Flask(__name__)

@app.route('/')
def my_form():
    #main()
    return render_template('my-form.html')

@app.route('/generate', methods = ['POST', 'GET'])
def get_by_category():
    text = request.args.get("text") #"this bird is black with yellow tail" #request.args.get("text")
    iterator = int(request.args.get("number"))
    print('---------------',text,'------------------',iterator,'--------------------')
    try:
        flag = main(text, iterator)
        if(flag):
            path = 'D:/AttnGAN/AttnGAN-Py3/AttnGAN/models/bird_AttnDCGAN2/from_text'
            #'D:/AttnGAN/AttnGAN-Py3/AttnGAN/models/bird_AttnDCGAN2/from_text/'
            temp_list = os.listdir(path)
            #while True:
            #    temp_list = os.listdir(path)
            #    if((os.path.exists(path))): #and  (len(temp_list) == 50)):
            #        print(os.listdir(path))
            #        break
            #    else:
            #        continue
            #print('after iterator--------')
            #if(os.listdir(path) == []):
            #    print('inner ifffffffffffff')
            #    raise Exception("No Images Generated")
            print('----after list checker----------')
            for i in range(len(temp_list)):
                temp_list[i] = path+temp_list[i]

            print(temp_list)
            dict1 = {}
            dict1['imgs'] = temp_list
            dict1['path'] = 'value'
            response = jsonify(message=dict1)
            print('------jsnonify--------')
            ##response = flask.jsonify({'some': 'data'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
            #print(response)
            #print('----------responce--------')
            #return dumps({"path": 'D:/AttnGAN/AttnGAN-Py3/AttnGAN/models/bird_AttnDCGAN2/from_text'}), 200, {"Content Type": "application/json"}
        else:
            #print('elseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee') 
            raise Exception("Model load ERROR")
    except :
        print('excepttttttttttttttttttttt')
        return dumps({"error": "Model Load ERROR"}), 500, {"Content Type": "application/json"}

#@app.route('/next', methods=['POST', 'GET'])
#def my_form_post():
#    text = request.form['text']
#    processed_text = text.upper()
#    print(processed_text)
#    return processed_text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002)
    #main()