from flask import Flask, request, jsonify
import requests
# import os
# from dotenv import load_dotenv
# import os

app = Flask(__name__)

@app.route('/', methods =['POST', 'GET']) 
def weather(): 
    if request.method == 'POST': 
        city = request.form.get('city') 
    else: 
        # for default name tampa
        city = 'tampa'

    # load_dotenv() 
    # your API key will come here 
    api_key = '48a90ac42caa09f90dcaeee4096b9e53'
    # source contain json data from api 
    resp = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}')


    # check out a JSON object to a python dictionary
    list_of_data = resp.json()
  
    # prepare the response for the UI request
    data = { 
        "country_code": str(list_of_data['sys']['country']), 
        "temp": str(list_of_data['main']['temp']),
        "temp_cel": '{:.2f}'.format(list_of_data['main']['temp'] - 273),
        "pressure": str(list_of_data['main']['pressure']), 
        "humidity": str(list_of_data['main']['humidity']), 
        "cityname": city,
    } 
    return jsonify(data)

app.run(debug=True, host='0.0.0.0', port=8080)
