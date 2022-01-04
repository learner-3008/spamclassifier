import requests
import json
from flask import Flask, request, jsonify, render_template, url_for

app = Flask(__name__)
app.static_folder='static'
url = "http://50559e1d-822c-4de5-ae92-159ffd38c6b2.eastus2.azurecontainer.io/score"

@app.route('/')
def home():
    #return 'Hello World'
    return render_template('home.html')

global result
result=""

@app.route('/predict',methods = ['POST'])
def predict():
    int_features =request.form.values()
    payload = json.dumps({
    "Inputs": {
        "WebServiceInput0": [
        {
            "v2": "{}".format(int_features)
        }
        ]
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 7AuqVm5WVxhbEkQEbkSDdVLDIKiVaSd8'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    out=json.loads(response.text)
    if out["Results"]["WebServiceOutput0"][0]["Scored Labels"] :
        result="SPAM"
    else:
        result="NOT SPAM"
    print(out["Results"]["WebServiceOutput0"][0])

    #output = round(prediction[0], 2)
    return render_template('home.html', prediction_text="The Message is {}".format(result))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    payload = json.dumps({
    "Inputs": {
        "WebServiceInput0": [
        {
            "v2": "{}".format(data.values())
        }
        ]
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 7AuqVm5WVxhbEkQEbkSDdVLDIKiVaSd8'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    output = response
    return jsonify(output)

if __name__ == '__main__':
    app.static_folder='static'
    app.run(debug=True)