# To guess: curl -X POST -d "player=ollie&number=10&password=ollie" http://127.0.0.1:8080/guess
# password will be saved at first call by that player, and the same player must use the same password every time

import flask
from flask import request, jsonify
import random
import jinja2


MAX_NUM = 20

app = flask.Flask(__name__)

answer = random.randint(1, 20)

all_guesses = {}
player_passwords = {}


# {% ... %} for Statements
# {{ ... }} for Expressions to print to the template output
# side note: in html, <tr> stands for"table row".  
# <tr> tag contains one or more <td> (table data) or <th> (table header) elements, which represent the individual cells within that row.

leaderboard_template = jinja2.Template("""
<font size="6">  
  Guess a number between 1 to {{ max_num }}
</font>
<br />
<br />
<table>
  <caption>
    <font size="5">Leaderboard</font size>
  </caption>
  <tr>
    <th>Player</th>
    <th>Guess</th>
  </tr>
  {% for item in data %}
  <tr>
    <td>{{ item.player }}</td>
    <td>{{ item.guess }}</td>
    {% if item.won %}
    <td> WINNER!!! </td>
    {% endif %}
  </tr>
  {% endfor %}
</table>
""")



@app.get('/leaderboard')
def leaderboard():
    leaderboard = sorted(
        [(k, v, abs(v - answer)) for k, v in all_guesses.items()],
        key=lambda x: x[2],
    ) #

    return leaderboard_template.render(
        data=[{'player': p, 'guess': g, 'won': diff == 0} for p, g, diff in leaderboard],
        max_num=MAX_NUM)

# optional status codes - 400: bad request for invalid syntax; 401: authentication error; 200, success
@app.post('/guess')
def guess_post():
    player = request.form['player']
    number = request.form['number']
    password = request.form['password']
    if not number.isnumeric():
        return f'Invalid number: {number}', 400
    
    if player in player_passwords:
        if player_passwords[player] != password:
            return "Wrong password!", 401
    else:
        player_passwords[player] = password
    
    all_guesses[player] = int(number)
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
