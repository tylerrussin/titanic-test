# Importing needed libraries
import uuid
from decouple import config
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from sklearn.externals import joblib
import traceback
import pandas as pd
import numpy as np
from flask_sqlalchemy import SQLAlchemy

# Saving DB var
DB = SQLAlchemy()

# Reads key value pair from .env
load_dotenv()

# Running function to create the app
def create_app():
    '''
    Used to initiate the app
    '''
    # saving flask(__name__) to var app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app) 

    @app.route('/predict', methods=['POST'])
    def predict():
        if lr:
            try:
                json_ = request.json
                print(json_)
                query = pd.get_dummies(pd.DataFrame(json_))
                query = query.reindex(columns=model_columns, fill_value=0)

                prediction = list(lr.predict(query))

                return jsonify({'prediction': str(prediction)})

            except:

                return jsonify({'trace': traceback.format_exc()})
        else:
            print ('Train the model first')
            return ('No model here to use')

    if __name__ == '__main__':
        try:
            port = int(sys.argv[1]) # This is for a command-line input
        except:
            port = 12345 # If you don't provide any port the port will be set to 12345

        lr = joblib.load("model.pkl") # Load "model.pkl"
        print ('Model loaded')
        model_columns = joblib.load("model_columns.pkl") # Load "model_columns.pkl"
        print ('Model columns loaded')

        app.run(port=port, debug=True)
