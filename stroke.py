import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

strokeprediction=pd.read_csv("C:\\Users\\kunja\\Downloads\healthcare-dataset-strokeprediction.csv")

X=pd.DataFrame(strokeprediction.iloc[:,1:-1])
Y=pd.DataFrame(strokeprediction.iloc[:,-1])
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2)

Y_train=Y_train.values.ravel()

Healthcare=LogisticRegression(max_iter=5000)
Healthcare.fit(X_train,Y_train)

y_pred=Healthcare.predict(X_test)

print("accuracy",(Healthcare.score(X_test,Y_test)))

import pickle
filename='stroke.pkl'
pickle.dump(Healthcare,open(filename,'wb'))

import flask
import pickle
from flask import request,render_template
filename = 'stroke.pkl'
model = pickle.load(open(filename, 'rb'))

app = flask.Flask(__name__, template_folder='templates')

app.secret_key = 'super secret key'
#@app.route('/')
#def home():
#    return render_template('index.html')

@app.route('/',methods=["GET", "post"])
def function():
    prediction = 0
    result = '  '
    if request.method == "GET":
        return render_template('care.html')

    if request.method == "POST":
        if request.form.get("submit"):
            age = flask.request.form['age']
            avg_glucose_level = flask.request.form['glucose']
            h = float(flask.request.form['height'])
            w = float(flask.request.form['weight'])
            bmi = w / (h * h)
            gender = flask.request.form['gender']
            ever_married = flask.request.form['marital_status']
            residence = flask.request.form['residence']
            work_type = flask.request.form['work_type']
            smoking_status = flask.request.form['smoking_status']
            hypertension = flask.request.form['hypertension']
            heart_disease = flask.request.form['heart_disease']

            input_values = pd.DataFrame([[gender, age, hypertension, heart_disease, ever_married, work_type, residence,
                                     avg_glucose_level, bmi, smoking_status]],
                                   columns=['gender', 'age', 'hypertension', 'heart_disease', 'marital_status',
                                            'work_type', 'residence', 'glucose', 'bmi', 'smoking_status'], dtype=float)
            prediction = model.predict(input_values)
        if(prediction==0):
            result = "You are Healthy"
        else:
            result = "You are Unhealthy"
        return render_template('treatment.html', result=result)


app.run(debug=True)



