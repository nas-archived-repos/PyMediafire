import requests,hashlib,getpass,json
email =""
password = ""
application_id = ""
api_key = ''
response_format = ""
class Mediafire:
	def __init__(self,email,password,application_id,api_key,response_format):
		self.email = email
		self.password = password
		self.application_id = application_id
		self.api_key = api_key
		self.response_format = response_format

	def Authenticate(self):
		signature = hashlib.sha1(self.email+self.password+self.application_id+self.api_key).hexdigest()
		parameters = {'email':self.email,'password':self.password,'application_id':self.application_id,'signature':signature,'response_format':self.response_format}
		r = requests.get("https://www.mediafire.com/api/user/get_session_token.php",params=parameters)
		json = r.json()
		json = json['response']
		if (json['result'] == "Error"):
			return json["message"]
		else:
			session_token = json['session_token']
			return session_token

