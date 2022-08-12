import flask
import pickle
import pandas as pd
from flask import send_from_directory, Flask, render_template
import os

app = flask.Flask(__name__, template_folder='templates')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

                               
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html', original_input={}))
    if flask.request.method == 'POST':
        # Use pickle to load in the pre-trained model.
        with open(f'model/hotel_compra.pkl', 'rb') as f:
            model = pickle.load(f)

        tirada = flask.request.form['tirada']
        casilla = flask.request.form['casilla']
        valor_casilla = flask.request.form['valor_casilla']
        input_variables = pd.DataFrame([[tirada, casilla, valor_casilla]],
                               columns=['tirada', 'casilla', 'valor_casilla'],
                                       dtype=float)        
        prediction = model.predict(input_variables)[0]
        
        return flask.render_template('main.html',
                                     original_input={'tirada':tirada,
                                                     'casilla':casilla,
                                                     'valor_casilla':valor_casilla},
                                     result=prediction,
                                     )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)