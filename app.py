from flask import Flask,render_template,url_for,request
import pandas as pd
#import pickle
from sklearn.linear_model import LinearRegression

app=Flask(__name__)


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST', 'GET'])
def predict():
	df = pd.read_csv("50_Startups.csv")
	df = pd.get_dummies(df)

	regressor = LinearRegression()
	regressor.fit(df.drop(['Profit'],axis=1),df.Profit)

	if request.method == 'POST':
		rd=request.form['rdspend']
		adm=request.form['admin']
		mk=request.form['market']
		sta=request.form.get('state')
		if sta=='California':
			c=1
			f=0
			n=0
		elif sta=='Florida':
			c=0
			f=1
			n=0
		else:
			c=0
			f=0
			n=1


		pred=pd.DataFrame([[rd,adm,mk,c,f,n]],columns=['R&D Spend','Administration','Marketing Spend','State_California','State_Florida','State_New York'])
		my_pred=regressor.predict(pred)

	return render_template('result.html',prediction=my_pred)
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
