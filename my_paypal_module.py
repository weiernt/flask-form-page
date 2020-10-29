# Written by Wei Ern (Ryan) Tan for ENACTUS's Carbon Offset project.
# Please do not email me unless necessary, i might cry trying to fix my code.

import requests
import json, base64

class APIKeys:
	""""
	API keys and secret keys for Paypal's API, should have the following variables:
	- sandbox_client_id, sandbox_secret
	- client_id, secret

	"""

	"""keep these in a class to just be safe from global variables (imagine this is a struct lol), if more Oject Oriented is needed,
	can have the functions become methods in the class and do constructor things, but i cant really be arsed"""


	sandbox_client_id=""
	sandbox_secret=""

	client_id=""
	secret=""


def create_subscription_plan(access_token, price, url="https://api.paypal.com/v1/billing/plans"):
	""""""
	# remember to eventually change the product_id, name etc
	# note this is currently using the sandbox's product ID so wont work using api.paypal, need sandbox.
	payload = "{\r\n  \"product_id\": \"PROD-100975334U790754Y\",\r\n  \"name\": \"Carbon Offset Subscription Plan\",\r\n  \"description\": \"Carbon Offset Subscription Plan, subscribed using the Carbon Offset Form, in AUD.\",\r\n  \"status\": \"ACTIVE\",\r\n  \"billing_cycles\": [\r\n    {\r\n      \"frequency\": {\r\n        \"interval_unit\": \"MONTH\",\r\n        \"interval_count\": 1\r\n      },\r\n      \"tenure_type\": \"REGULAR\",\r\n      \"sequence\": 1,\r\n      \"total_cycles\": 12,\r\n      \"pricing_scheme\": {\r\n        \"fixed_price\": {\r\n          \"value\": \"" + str(price) + "\",\r\n          \"currency_code\": \"AUD\"\r\n        }\r\n      }\r\n    }\r\n  ],\r\n  \"payment_preferences\": {\r\n    \"auto_bill_outstanding\": true,\r\n    \"setup_fee_failure_action\": \"CONTINUE\",\r\n    \"payment_failure_threshold\": 3\r\n  }\r\n}"
	
	headers = {}
	headers['Authorization']= 'Bearer ' + access_token
	headers['Accept'] 	    = 'application/json'
	headers['Content-Type'] = 'application/json'
	
	response = requests.request("POST", url, headers=headers, data = payload)
	response_json = json.loads(response.text.encode("utf-8"))
	plan_id = response_json["id"]
	# print(response_json)
	return plan_id

def create_sandbox_subscription_plan(access_token, price):
	# receives price parameter, returns plan_id
	
	url = "https://api.sandbox.paypal.com/v1/billing/plans"

	return create_subscription_plan(access_token, price, url)
	

def get_access_token(client_id=None, secret=None, url="https://api.paypal.com/v1/oauth2/token"):
	"""
		
	"""
	# NEED TO CHANGE THIS TO USING REAL CIENTID AND SECRET KEYS from my class
	if client_id==None and secret==None:
		client_id = APIKeys.sandbox_client_id
		secret    = APIKeys.sandbox_secret
	combined = client_id + ":" + secret
		
	payload = 'grant_type=client_credentials'
	
	headers = {}
	# encodes the CLIENT_ID and SECRET into base64
	headers['Authorization'] = 'Basic ' + str(base64.b64encode(combined.encode("utf-8")), "utf-8")
	headers['Content-Type']  = 'application/x-www-form-urlencoded'
	

	response = requests.request("POST", url, headers=headers, data = payload)
	response_json = json.loads(response.text.encode("utf-8"))
	access_token = response_json["access_token"]
	return access_token

def get_sandbox_access_token(client_id=None, secret=None):
	"""
		
	"""
	
	# assert(type(client_id)==str and type(secret)==str)
	if client_id==None and secret==None:
		client_id = APIKeys.sandbox_client_id
		secret    = APIKeys.sandbox_secret
	combined = client_id + ":" + secret
	
	url = "https://api.sandbox.paypal.com/v1/oauth2/token"

	return get_access_token(client_id, secret, url)
	
	
def get_subscription_plans(access_token, url="https://api.paypal.com/v1/billing/plans"):
	""" make it take an optional input url so you only need to edit/make changes to 1 function (ideally)"""
	payload = {}

	headers = {}
	headers['Authorization'] = 'Bearer ' + access_token
	headers['Prefer'] 		 = 'return=representation'
	

	response = requests.request("GET", url, headers=headers, data = payload)
	vae = json.loads(response.text.encode('utf8'))
	print(json.dumps(vae, indent=4))

def get_sandbox_subscription_plans(access_token):
	# purely for testing purposes, use to check for subscription plans
	url = "https://api.sandbox.paypal.com/v1/billing/plans"
	get_subscription_plans(access_token, url)


	
def deactivate_sandbox_plan(access_token, plan_id):
	"""Seems like you can't delete old subscription plans so just ignore i guess"""
	url= f"https://api.sandbox.paypal.com/v1/billing/plans/{plan_id}/deactivate"
	
	headers = {}
	headers["Authorization"] = "Bearer " + access_token
	headers["Content-Type"]  = "application/json"
	
	response = requests.request("POST", url, headers=headers)
	vae = json.loads(response.text.encode('utf8'))
	print(json.dumps(vae, indent=4))
	
def get_products(access_token, url="https://api.paypal.com/v1/catalogs/products"):
	"""just use for testing purposes to see if there is product there"""

	payload = {}
	headers = {}
	headers['Authorization'] = 'Bearer ' + access_token

	response = requests.request("GET", url, headers=headers, data = payload)
	received_json = json.loads(response.text.encode('utf8'))
	print(received_json["products"])

def get_sandbox_products(access_token):
	"""just use for testing purposes to see if there is product there"""
	url = "https://api.sandbox.paypal.com/v1/catalogs/products"

	payload = {}
	headers = {}
	headers['Authorization'] = 'Bearer ' + access_token

	response = requests.request("GET", url, headers=headers, data = payload)
	received_json = json.loads(response.text.encode('utf8'))
	print(received_json["products"])

def create_product(access_token, url="https://api.paypal.com/v1/catalogs/products"):
	payload = "{\r\n    \"name\": \"Carbon Offsets\",\r\n    \"type\": \"SERVICE\"\r\n}"
	headers = {
	'Authorization': 'Bearer ' + access_token,
	'Content-Type': 'application/json'
	}

	response = requests.request("POST", url, headers=headers, data = payload)

	print(response.text.encode('utf8'))

def create_sandbox_product(access_token):
	"""Note that products arent the same as subscription, subscriptions sell a product
	So i'm thinking to manually create the product then never change it again"""

	url = "https://api.sandbox.paypal.com/v1/catalogs/products"

	payload = "{\r\n    \"name\": \"Carbon Offsets\",\r\n    \"type\": \"SERVICE\"\r\n}"
	headers = {
	'Authorization': 'Bearer ' + access_token,
	'Content-Type': 'application/json'
	}

	response = requests.request("POST", url, headers=headers, data = payload)

	print(response.text.encode('utf8'))


if __name__=="__main__":
	
	# get_sandbox_products(get_sandbox_access_token())
	product_id = "PROD-2MB55916MR702342V"

	# then print subscription plans
	access_token = get_access_token(client_id=APIKeys.client_id, secret=APIKeys.secret)
	print(get_subscription_plans(access_token=get_access_token(client_id=APIKeys.client_id, secret=APIKeys.secret))) #yup shows correct
	print(access_token)


	