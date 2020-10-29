from flask import Flask, render_template, request, flash, session
from wtforms import Form, TextField, RadioField, validators, FormField, FieldList
from wtforms.fields.html5 import EmailField, IntegerField

import json
import requests
import sys
import csv

import my_paypal_module
from my_paypal_module import APIKeys
import my_csv_library




app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_super_secret_key' # Should just generate random key here for security purposes, but this works crudely.



	
class FieldsRequiredForm(Form):
    """Require all fields to have content. This works around the bug that WTForms radio
    fields don't honor the `DataRequired` or `InputRequired` validators.

	Copy pasted (with tiny modification) from a github issue on WTForms, 
	just inherit straight from this rather than the usual wtforms.Form
    """

    class Meta:
        def render_field(self, field, render_kw):
            render_kw.setdefault('required', True)
            return super().render_field(field, render_kw)

class MyIntegerField(IntegerField):
	"""My use case for IntegerField requires InputRequired() and set the class='form-control' for bootsrap
		Note this is using HTML5's type="number" input
	"""
	def __init__(self, label="", validators=[validators.InputRequired()], render_kw={"class":"form-control", "min":"0"}, **kwargs ):
		super(MyIntegerField, self).__init__(label, validators, render_kw=render_kw, **kwargs)

class MyRadioField(RadioField):
	"""Not sure why render_kw not working here, but just create my own radiofield so all have InputRequired()"""
	def __init__(self, label="", validators=[validators.InputRequired()], **kwargs):
		super(MyRadioField, self).__init__(label, validators, **kwargs)

class CarbonOffsetIntegerForm(FieldsRequiredForm):
	"""Follows exactly the variable names from the ucalc.pro calculator"""

	B = MyIntegerField("IN AN AVERAGE WEEK, ROUGHLY how many kilometres do you drive or ride in a car? (including rideshare apps?)")
	
	AH = MyIntegerField("IN AN AVERAGE YEAR, ROUGHLY HOW MANY KILOMETRES DO YOU FLY DOMESTICALLY?")
	
	AI = MyIntegerField("IN AN AVERAGE YEAR, ROUGHLY HOW MANY KILOMETRES DO YOU FLY INTERNATIONALLY?")
	
	F = MyIntegerField("On average, how many kilometres do you travel by train per week?")
	
	D = MyIntegerField("On average, how many kilometres do you travel by tram per week?")
	
	H = MyIntegerField("On average, how many of your meals contain red meat per week?")
	
	M = MyIntegerField("On average, how many of your meals contain poultry OR chicken per week?")
	
	AF = MyIntegerField("ON AVERAGE, how many EGGS DO YOU CONSUME PER WEEK?")
	
	L = MyIntegerField("On average, how many of your meals contain dairy milk products per week?")
	
	K = MyIntegerField("On average, how many of your meals contain bread, flour and cereal products per week?")
	
	J = MyIntegerField("On average, how many times do you eat miscellaneous snacks (e.g. small packaged foods, chips, confectionery, etc.) per week?")
	
	I = MyIntegerField("On average, how many times do you consume alcohol per week?")

class CarbonOffsetRadioForm(FieldsRequiredForm): 
	# 1,2,3,4,5+ (value, label)
	Rchoices = [(3086, "1"), (4526, "2"), (5262, "3"), (5782, "4"), (6305, "5+")] 
	R = MyRadioField("How many PEOPLE live in your household?", choices=Rchoices )
	
	#yes or no
	Uchoices = [(4076, "Yes"), (0, "No")]
	U = MyRadioField("Does your property have a pool?", choices=Uchoices)
	
	Xchoices = [(-1335.36, "1 kWh"), (-2003.05, "1.5kWh"), (-4006.08, "3kWh"),
            	(-5341.3, "4kWh"), (0, "My household has no solar system installed"),
				(-3171.45, "I have solar panels, I'm just not sure what size system I have!")]
	X = MyRadioField("If your household does have solar panels installed, roughly what size solar system do you have?",
				     choices=Xchoices)
	
	AAchoices = [(1.47, "Well below average"), (1.89, "Below average"), 
			     (2.1, "About average"), (2.31, "Above average"), 
				 (2.73, "Well above average")]			 
	AA = MyRadioField("How much waste do you think you produce, relative to the average Australian? \
				      (i.e. the average Australian produces 5.6 kgs of waste per day)",
					  choices=AAchoices)
	
	ABchoices = [(0.25, "25%"), (0.475, "50% (5% discount)"), (0.6375, "75% (15% discount)"), (0.8, "100% (go carbon neutral with a 20% discount!)"),
	      	     (1, "125% (go carbon positive with a 20% discount!)"), (1.2, "150% (20% discount)")]		  
	AB = MyRadioField("Select the proportion of your carbon footprint you would like to offset - note that the more you offset, the bigger discount your receive!.",
					  choices=ABchoices)

class CarbonOffsetEmailForm(FieldsRequiredForm):
	email = EmailField("Please enter your email:", validators=[validators.InputRequired()], render_kw={"class":"form-control"})

class CarbonOffsetNameForm(FieldsRequiredForm):
	first_name = TextField("First name: ", validators=[validators.InputRequired()], render_kw={"class":"form-control"})
	last_name = TextField("Last name: ", validators=[validators.InputRequired()], render_kw={"class":"form-control"})
	#TODO: price, and carbon emissions add
	

class MainForm(FieldsRequiredForm):
	integer_fields = FormField(CarbonOffsetIntegerForm)

	radio_fields = FormField(CarbonOffsetRadioForm)

	email_fields = FormField(CarbonOffsetEmailForm)

	name_fields = FormField(CarbonOffsetNameForm)
	
@app.route("/", methods=["GET", "POST"])
@app.route("/paypal_page", methods=["GET", "POST"])
def paypal_page():
	main_form = MainForm(request.form)
	plan_id = 0
	price_per_month = 0
	carbon_footprint = 0
	
	# Create subscription plan here after received price, then return the plan_id back to form
	if request.method=="POST":
		# rip formatting this
		print(request.form)
		# formating of the names is <field_name>-<variable name>
		B     = float(request.form['integer_fields-B'])
		AH	  = float(request.form['integer_fields-AH'])
		AI	  = float(request.form['integer_fields-AI'])
		F 	  = float(request.form['integer_fields-F'])
		D	  = float(request.form['integer_fields-D'])
		H	  = float(request.form['integer_fields-H'])
		M	  = float(request.form['integer_fields-M'])
		AF	  = float(request.form['integer_fields-AF'])
		L	  = float(request.form['integer_fields-L'])
		K	  = float(request.form['integer_fields-K'])
		J	  = float(request.form['integer_fields-J'])
		I	  = float(request.form['integer_fields-I'])
		R	  = float(request.form['radio_fields-R'])
		U	  = float(request.form['radio_fields-U'])
		X	  = float(request.form['radio_fields-X'])
		AA	  = float(request.form['radio_fields-AA'])
		AB	  = float(request.form['radio_fields-AB'])
		# yea not currently using email, but can be saved to database for something in future.
		email = request.form['email_fields-email']
		first_name = request.form['name_fields-first_name']
		last_name = request.form['name_fields-last_name']
		
		if main_form.validate():
			# NOTE: need to change formula for price per month in both main.py and JS files,
			#  is probably possible to straight send POST request to paypal from 
			#  javascript but I had started this project using flask so I was too lazy to do it again in js.

			carbon_footprint = (B*0.000174+D*0.00012+F*0.00002+((AH*0.00009747)/189)+((AI*0.0001111)/150)+(H*0.0084)+(I*0.00044)+(J*0.00112)+(K*0.00063)+(L*0.00072)+(M*0.00024)+(AF*0.00002)+(R+U+X)*0.00102+(AA*1.6917))/12
			price_per_month = carbon_footprint * AB * 25 * 1.29 

			# round them to 2 decimal places
			price_per_month = round(price_per_month,2)
			carbon_footprint = round(carbon_footprint, 2)

			# create plan here, REMEMBER TO change to APIKEYS.client_id when I get enactus's paypal.

			if not (my_csv_library.check_csv()):
				#csv does not exists
				my_csv_library.init_csv()



			access_token= my_paypal_module.get_access_token(APIKeys.client_id, APIKeys.secret)
			plan_id = my_paypal_module.create_subscription_plan(access_token, price_per_month)
			# flash(f"Based on your monthly carbon footprint of {carbon_footprint:.2f} tonnes per month, your generated subscription price is ${price_per_month:.2f}. This subscription is cancellable at any time - take the next step towards creating a greener tomorrow! We'll reach out to you within 24 hours of your order to confirm your impact! ")
			# flash({
			# 		"subscription_msg": f"Based on your monthly carbon footprint of {carbon_footprint:.2f} tonnes per month, your generated subscription price is ${price_per_month:.2f}.",
			# 		"terms_and_cond": "This subscription is cancellable at any time - take the next step towards creating a greener tomorrow! We'll reach out to you within 24 hours of your order to confirm your impact! "
			# 		})

			# takes in names, email, price of subscription, carbonfootprint (tonnes per month), the created plan_id, and proportion they chose to offset
			my_csv_library.add_row(first_name, last_name, email, price_per_month, carbon_footprint, plan_id, AB)




			# note this also needs to pass in a client_id param for the paypal button, also passing in carbon_footprint and price_permonth to flash to customers.
	return render_template("paypal_page.html", main_form=main_form,
							price_per_month=price_per_month, carbon_footprint=carbon_footprint,
							plan_id=plan_id, client_id=APIKeys.client_id)
	

# @app.route("/ENACTUS_MYCARBON_SECRET_PAGE")
# def csv_page():
# 	# ONLY displays the csv data if you enter exactly the way needed
# 	if request.args.get("password")==CSV_PASSWORD:

# 		# this commented out one was for testing
# 		# with open("./csv_stuff/csv_file.csv", "r", newline="") as f:
# 		with open(my_csv_library.PROJECT_HOME + "/csv_stuff/csv_file.csv", "r", newline="") as f:

# 			r = csv.reader(f)
# 			csv_data = list(r)

# 		return render_template("secret.html", data=csv_data)
# 	return

	
if __name__=="__main__":
	app.run(debug=True)





