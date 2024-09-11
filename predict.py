from flask import Flask, request
import pickle
import sklearn

app = Flask(__name__) 

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

with open("./artefacts/classifier.pkl", 'rb') as model_file:
    clf = pickle.load(model_file) 

@app.route("/predict",methods=['POST'])
def prediction():
    # Pre-processing user input
    loan_req = request.get_json()
    print(loan_req)

    if loan_req['Gender'] == "Male":
        Gender = 0
    else:
        Gender = 1

    if loan_req['Married'] == "Unmarried":
        Married = 0
    else:
        Married = 1

    if loan_req['Credit_History'] == "Unclear Debts":
        Credit_History = 0
    else:
        Credit_History = 1

    ApplicantIncome = loan_req['ApplicantIncome']
    LoanAmount = loan_req['LoanAmount'] / 1000

    # Making predictions
    prediction = clf.predict(
        [[Gender, Married, ApplicantIncome, LoanAmount, Credit_History]])

    if prediction == 0:
        pred = 'Rejected'
    else:
        pred = 'Approved'
    return {"loan_approval_status": pred} 
