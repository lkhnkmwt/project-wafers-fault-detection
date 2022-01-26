from flask import Flask, request, render_template
from flask_cors import CORS,cross_origin
from prediction_Validation_Insertion import pred_validation
from predictFromModel import prediction
import json
app=Flask(__name__)
CORS(app)


@app.route('/',methods=['GET','POST'])
@cross_origin()
def homepage():
    return render_template('index.html')

@app.route('/value',methods=['GET','POST'])
def valuepage():
    try:
        if request.method == 'POST':
            path = request.form['filepath']
            pred_val = pred_validation(path)  # object initialization

            pred_val.prediction_validation()  # calling the prediction_validation function

            pred = prediction(path)  # object initialization

            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()
            return ("Prediction File created at !!!" + str(path) + 'and few of the predictions are ' + str(json.loads(json_predictions)))
        else:
            print('Nothing Matched')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    app.run()