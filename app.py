from flask import Flask, redirect,render_template,url_for,request,jsonify
from flask_cors import cross_origin
import pandas as pd
import numpy as np
import datetime
import pickle

edited_row_dataset = pd.read_csv("flood2_date - flood2_date.csv")

app = Flask(__name__, template_folder="template")
model = pickle.load(open("models\IFI_After_review2.pkl", "rb"))
# print("Model Loaded")

@app.route("/",methods=['GET'])
@cross_origin()
def home():
	return render_template("index.html")

@app.route("/predict",methods=['GET', 'POST'])
@cross_origin()
def predict():
	
	if request.method == 'GET':
		return render_template('predictor_2.html')
	elif request.method == "POST":
		

		# duration = request.form['Duration']
		area_affected = request.form['Area_affected']
		main_cause = request.form['Main_cause']
		# main_cause.insert(0,"Select Main Cause")

		input_data = []
		
		temp_main_cause=[]

# error handling
		# if not duration:
		# 	error_statement = "⚠️Duration Field Empty..."
		# 	# return render_template("/predictor.html", error_statement=error_statement,duration=duration,area_affected=area_affected,main_cause=main_cause)
		# 	return  error_statement
		if not area_affected:
			error_statement = "⚠️Area Affected Field Empty..."
			# return render_template( "/predictor.html",error_statement=error_statement,duration=duration,area_affected=area_affected,main_cause=main_cause)
			return  error_statement
		elif (main_cause == '0'):
			error_statement = "⚠️Main Cause Field Empty..."
			# return render_template("/predictor.html", error_statement=error_statement,duration=duration,area_affected=area_affected,main_cause=main_cause)
			return  error_statement
		
		if(main_cause == '1'):
			temp_main_cause=[1,0,0,0,0,0]
		elif(main_cause == '2'):
			temp_main_cause=[0,1,0,0,0,0]
		elif(main_cause == '3'):
			temp_main_cause=[0,0,1,0,0,0]
		elif(main_cause == '4'):
			temp_main_cause=[0,0,0,1,0,0]
		elif(main_cause == '5'):
			temp_main_cause=[0,0,0,0,1,0]	
		elif(main_cause == '6'):
			temp_main_cause=[0,0,0,0,0,1]



	# input_data = [duration,area_affected,0,1,0,0,0,0]

	# input_data = [duration,area_affected,*temp_main_cause]
	# input_data_as_numpy_array = np.asarray(input_data)

	# input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

	# prediction1 = model.predict(input_data_reshaped)



	# 2nd approach to for applying model
		print(temp_main_cause)
		temp=[area_affected]
		temp.extend(temp_main_cause)
		print(temp)
		prediction1= model.predict(pd.DataFrame([temp ] , columns = ['Area Affected','Main Cause_Dam/Levy, break or release','Main Cause_Extra-tropical Cyclone','Main Cause_Heavy Rain','Main Cause_Monsoonal Rain','Main Cause_Torrential Rain','Main Cause_Tropical Cyclone']))
		# print(prediction1)
	

		# output_string=""
		if (prediction1[0]==2):
			output_string="Prediction :🔴Heavy Flood will occur❗ ❗ ❗ ❗"
			# return render_template("yes_flood.html")
			# return redirect('/')
		elif (prediction1[0]==1):
			output_string="Prediction :🟡Chances of Flood"
		else:
			output_string="Prediction :🟢Flood will not occur "
			# return render_template("no_flood.html")
			# return redirect('/')
		return output_string

# @app.route("/predict",methods=['POST'])


@app.route('/about_us', methods=['GET', 'POST'])
def about_us():
	return render_template("about_us.html")

@app.route('/faq1', methods=['GET', 'POST'])
def faq1():
	return render_template("faq1.html")

@app.route('/visualiztion')
def visualiztion():
	# return render_template("virtual_graphs_anish.html")
	return render_template("dashboard_page.html")


if __name__=='__main__':
	app.run(debug=True)