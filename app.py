from flask import Flask,render_template, url_for ,flash , redirect
import joblib
from flask import request
import pandas as pd
import re
from bs4 import BeautifulSoup



app=Flask(__name__,template_folder='template')

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'

def preprocess(q):

    q = str(q).lower().strip()

    # Replace certain special characters with their string equivalents
    q = q.replace('%', ' percent')
    q = q.replace('$', ' dollar ')
    q = q.replace('₹', ' rupee ')
    q = q.replace('€', ' euro ')
    q = q.replace('@', ' at ')


    # Replacing some numbers with string equivalents (not perfect, can be done better to account for more cases)
    q = q.replace(',000,000,000 ', 'b ')
    q = q.replace(',000,000 ', 'm ')
    q = q.replace(',000 ', 'k ')
    q = re.sub(r'([0-9]+)000000000', r'\1b', q)
    q = re.sub(r'([0-9]+)000000', r'\1m', q)
    q = re.sub(r'([0-9]+)000', r'\1k', q)

    # Decontracting words
    # https://en.wikipedia.org/wiki/Wikipedia%3aList_of_English_contractions
    # https://stackoverflow.com/a/19794953
    contractions = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "can not",
    "can't've": "can not have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
    }

    q_decontracted = []

    for word in q.split():
        if word in contractions:
            word = contractions[word]

        q_decontracted.append(word)

    q = ' '.join(q_decontracted)
    q = q.replace("'ve", " have")
    q = q.replace("n't", " not")
    q = q.replace("'re", " are")
    q = q.replace("'ll", " will")

    # Removing HTML tags
    q = BeautifulSoup(q)
    q = q.get_text()

    # Remove punctuations
    pattern = re.compile('\W')
    q = re.sub(pattern, ' ', q).strip()
    q = re.sub(' +', ' ', q)
    q = q.replace('\r', '').replace('\n', '')


    return q



@app.route("/")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/home_loan")
def home_loan():
    return render_template("home_loan.html")

@app.route("/term_deposit")
def term_deposit():
    return render_template("term_deposit.html")

@app.route("/customer_churn")
def customer_churn():
    return render_template("customer_churn.html")

@app.route("/personal_loan")
def personal_loan():
    return render_template("personal_loan.html")

@app.route("/loan_default")
def loan_default():
    return render_template("loan_default.html")

@app.route("/finance_sentiment")
def finance_sentiment():
    return render_template("Finance_sentiment.html")
    

@app.route('/predict_home_loan', methods=['POST'])
def predict_home_loan():
    if request.method == 'POST':
        Gender = int(request.form['Gender'])
        Married = int(request.form['Married'])
        Dependents = (request.form['Dependents'])
        Graduate = int(request.form['Graduate'])
        Self_Employed = int(request.form['Self_Employed'])
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])
        Credit_History = int(request.form['Credit_History'])
        Property_Area = (request.form['Property_Area'])

        final_pipe = joblib.load('Pipelines/home_loan_approval_prediction_pipeline')

        test = pd.DataFrame(columns=['Gender', 'Married', 'Dependents', 'Graduate', 'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
                                       'Loan_Amount_Term', 'Credit_History', 'Property_Area'])

        test.loc[0] = [Gender, Married, Dependents, Graduate, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area]
        home_loan_model = joblib.load('Models/home_loan_approval_prediction_model')
        result = home_loan_model.predict(final_pipe.transform(test))

        if (int(result[0]) == 1):
            prediction = 'Congrats ! you are Eligible for Home Loan'
        else:
            prediction = 'Sorry ! you are not Eligible for Home Loan'

        return render_template('result.html', prediction=prediction)
        

@app.route('/predict_customer_churn', methods=['POST'])
def predict_customer_churn():
    if request.method == 'POST':
        CreditScore = int(request.form['CreditScore'])
        Geography = (request.form['Geography'])
        Gender = (request.form['Gender'])
        Age = int(request.form['Age'])
        Tenure = int(request.form['Tenure'])
        Balance = float(request.form['Balance'])
        NumOfProducts = int(request.form['NumOfProducts'])
        HasCrCard = int(request.form['HasCrCard'])
        IsActiveMember = int(request.form['IsActiveMember'])
        EstimatedSalary = float(request.form['EstimatedSalary'])
        
        final_pipe = joblib.load('Pipelines/bank_customer_churn_pipelines')

        test = pd.DataFrame(columns=['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure',
                                      'Balance', 'NumOfProducts', 'HasCrCard','IsActiveMember','EstimatedSalary'])
        test.loc[0] = [CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary]
        customer_churn_model = joblib.load('Models/bank_customer_churn_model')
        result = customer_churn_model.predict(final_pipe.transform(test))

        if (int(result[0]) == 1):
            prediction = 'Oops ! this customer may exit the bank'
        else:
            prediction = 'Congrats ! this customer is loyal'

        return render_template('result.html', prediction=prediction)


@app.route('/predict_term_deposit', methods=['POST'])
def predict_term_deposit():
    if request.method == 'POST':
        age = int(request.form['age'])
        job = (request.form['job'])
        marital = (request.form['marital'])
        education = (request.form['education'])
        default = (request.form['default'])
        housing = (request.form['housing'])
        loan = (request.form['loan'])
        contact = (request.form['contact'])
        month = (request.form['month'])
        day_of_week = (request.form['day_of_week'])
        duration = int(request.form['duration'])
        campaign = int(request.form['campaign'])
        pdays = int(request.form['pdays'])
        previous = int(request.form['previous'])
        poutcome = (request.form['poutcome'])
        emp_var_rate = float(request.form['emp_var_rate'])
        cons_price_idx = float(request.form['cons_price_idx'])
        cons_conf_idx = float(request.form['cons_conf_idx'])
        euribor3m = float(request.form['euribor3m'])
        nr_employed = float(request.form['nr_employed'])

        final_pipe = joblib.load('Pipelines/bank_marketing_pipeline')

        test = pd.DataFrame(columns=['age', 'job', 'marital', 'education',
                                      'default', 'housing', 'loan',
                                      'contact', 'month', 'day_of_week',
                                      'duration', 'campaign', 'pdays', 'previous', 'poutcome',
                                      'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m',
                                      'nr.employed'])
        test.loc[0] = [age, job, marital, education, default, housing, loan, contact,
                       month, day_of_week, duration, campaign, pdays, previous, poutcome, emp_var_rate,
                       cons_price_idx, cons_conf_idx, euribor3m, nr_employed]
        term_deposit_model = joblib.load('Models/bank_marketing_model')
        result = term_deposit_model.predict(final_pipe.transform(test))

        if (int(result[0]) == 1):
            prediction = "Great ! this customer may be interested in term deposit, guys it's a lead"
        else:
            prediction = 'Oops ! this customer may not be interested in term deposit'

        return render_template('result.html', prediction=prediction)

# Income	Age	Experience	Married_or_Single	House_Ownership	Car_Ownership	Profession	CITY	STATE	CURRENT_JOB_YRS	CURRENT_HOUSE_YRS

@app.route('/predict_loan_default', methods=['POST'])
def predict_loan_default():
    if request.method == 'POST':
        Income = float(request.form['Income'])
        Age = int(request.form['Age'])
        Experience = int(request.form['Experience'])
        Married_or_Single = (request.form['Married_or_Single'])
        House_Ownership = (request.form['House_Ownership'])
        Car_Ownership = (request.form['Car_Ownership'])
        Profession = (request.form['Profession'])
        CITY = (request.form['CITY'])
        STATE = (request.form['STATE'])
        CURRENT_JOB_YRS = float(request.form['CURRENT_JOB_YRS'])
        CURRENT_HOUSE_YRS = float(request.form['CURRENT_HOUSE_YRS'])

        final_pipe = joblib.load('Pipelines/indian_loan_default_prediction_pipeline')

        test = pd.DataFrame(columns=['Income', 'Age', 'Experience', 'Married/Single', 'House_Ownership', 'Car_Ownership',
                                     'Profession', 'CITY', 'STATE', 'CURRENT_JOB_YRS', 'CURRENT_HOUSE_YRS'])
        test.loc[0] = [Income, Age, Experience, Married_or_Single, House_Ownership, Car_Ownership, Profession, CITY, STATE,
                       CURRENT_JOB_YRS, CURRENT_HOUSE_YRS]
        loan_default_model = joblib.load('Models/indian_loan_default_prediction_model')
        result = loan_default_model.predict(final_pipe.transform(test))

        if (int(result[0]) == 1):
            prediction = 'Got him ! this customer is gonna default the loan'
        else:
            prediction = 'Great ! this customer is not gonna default the loan'

        return render_template('result.html', prediction=prediction)


@app.route('/predict_personal_loan', methods=['POST'])
def predict_personal_loan():
    if request.method == 'POST':
        Age = int(request.form['Age'])
        Experience = int(request.form['Experience'])
        Income = float(request.form['Income'])
        ZIP_Code = int(request.form['ZIP_Code'])
        Family = int(request.form['Family'])
        CCAvg = float(request.form['CCAvg'])
        Education = int(request.form['Education'])
        Mortgage = int(request.form['Mortgage'])
        Securities_Account = int(request.form['Securities_Account'])
        CD_Account = int(request.form['CD_Account'])
        Online = int(request.form['Online'])
        CreditCard = int(request.form['CreditCard'])

        final_pipe = joblib.load('Pipelines/bank_personal_loan_pipeline')

        test = pd.DataFrame(columns=['Age', 'Experience', 'Income', 'ZIP_Code', 'Family',
                                      'CCAvg', 'Education', 'Mortgage', 'Securities_Account',
                                      'CD_Account','Online','CreditCard'])
        test.loc[0] = [Age, Experience, Income, ZIP_Code, Family, CCAvg,
                       Education, Mortgage, Securities_Account, CD_Account,Online,CreditCard]
        personal_loan_model = joblib.load('Models/bank_personal_loan_model')
        result = personal_loan_model.predict(final_pipe.transform(test))

        if (int(result[0]) == 1):
            prediction = "Great ! this customer may be interested in buying personal, guys it's a lead"
        else:
            prediction = 'Oops ! this customer may not be interested in buying personal'

        return render_template('result.html', prediction=prediction)


@app.route('/predict_finance_sentiment', methods=['POST'])
def predict_finance_sentiment():
    if request.method == 'POST':
        vectorizer = joblib.load('Pipelines/finance_sentiment_vectorizer')
        finance_sentiment_classifier = joblib.load('Models/finance_sentiment_classifier')
        text = request.form['message']

        model_prediction = finance_sentiment_classifier.predict(vectorizer.transform([text]))

        finance_sentiment_labels = {0: "Neutral", 1: "Positive", -1: "Negative"}

        prediction = finance_sentiment_labels[model_prediction[0]]

        return render_template('result.html', prediction=prediction)


#if __name__ == "__main__":
#    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)