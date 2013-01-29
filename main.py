import requests,hashlib,getpass,json

email =""
password = ""
application_id = ""
api_key = ''
response_format = "json"
def Authenticate(email,password,application_id,response_format):
	signature = hashlib.sha1(email+password+application_id+api_key).hexdigest()
	parameters = {'email':email,'password':password,'application_id':application_id,'signature':signature,'response_format':response_format}
	r = requests.get("https://www.mediafire.com/api/user/get_session_token.php",params=parameters)
	json = r.json()
	json = json['response']
	if (json['result'] == "Error"):
		return json["message"]
	else:
		session_token = json['session_token']
		return session_token

x = Authenticate(email,password,application_id,response_format)
print x