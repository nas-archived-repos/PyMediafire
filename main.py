import requests,hashlib,getpass,json

email =""
password = ""
application_id = ""
api_key = ""
response_format = "json"

class Mediafire:
	def __init__(self,email,password,application_id,api_key,response_format="json"):
		self.email = email
		self.password = password
		self.application_id = application_id
		self.api_key = api_key
		self.response_format = response_format
		self.signature = hashlib.sha1(self.email+self.password+self.application_id+self.api_key).hexdigest()
		self.session_token=""


	def get_session_token(self):
		parameters = {'email':self.email,'password':self.password,'application_id':self.application_id,'signature':self.signature,'response_format':self.response_format}
		r = requests.get("https://www.mediafire.com/api/user/get_session_token.php",params=parameters)
		json = r.json()['response']
		if (json['result'] == "Error"):
			print json["message"]
		else:
			self.session_token = json['session_token']

	def renew_session_token(self):
		parameters = {'session_token':self.session_token,'response_format':self.response_format}
		r = requests.get("http://www.mediafire.com/api/user/renew_session_token.php",params=parameters)
		json = r.json()['response']
		if (json['result'] == "Error"):
			print json["message"]
		else:
			self.session_token = json['session_token']

	def get_login_token(self):
		parameters = {'email':self.email,'password':self.password,'application_id':self.application_id,'signature':self.signature,'response_format':self.response_format}
		r = requests.get("https://www.mediafire.com/api/user/get_login_token.php",params=parameters)
		json = r.json()['response']
		if (json['result'] == "Error"):
			print json["message"]
		else:
			self.login_token = json['login_token']
			self.login_url = "http://www.mediafire.com/api/user/login_with_token.php?login_token=" + self.login_token

	def register(self,email,password,first_name,last_name,display_name): #Does not work yet
		parameters = {'application_id':self.application_id,'email':email,'password':password,'response_format':self.response_format}
		r = requests.get("https://www.mediafire.com/api/user/register.php",params = parameters)
		json = r.json()["response"]
		if (json['result'] == "Error"):
			print json["message"]
		else:
			print "Registered user for " + email + " succesfully"

	def get_info(self):
		parameters = {'session_token':self.session_token,'response_format':self.response_format}
		r = requests.get("http://www.mediafire.com/api/user/get_info.php",params=parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			json = json['user_info']
			return json
	def update(self,display_name,first_name,last_name,birth_date,gender,website,location,newsletter,primary_usage):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'display_name':display_name,'first_name':first_name,'last_name':last_name,'birth_date':birth_date,'gender':gender,'website':website,'location':location,'newsletter':newsletter,'primary_usage':primary_usage}
		r = requests.get("http://www.mediafire.com/api/user/update.php",params=parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Updated succesfully"

	def myfiles_revision(self): #Still have to figure out how this works
		parameters = {'session_token':self.session_token,'response_format':self.response_format}
		r = requests.get("http://www.mediafire.com/api/user/myfiles_revision.php",params=parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			return json['revision']

	def fetch_tos(self): #I should find a way to display the actual terms of service
		parameters = {'session_token':self.session_token,'response_format':self.response_format}
		r = requests.get("http://www.mediafire.com/api/user/fetch_tos.php", params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			self.acceptance_token = json["terms_of_service"]["acceptance_token"]

	def accept_tos(self):
		parameters = {'session_token':self.session_token,'acceptance_token':self.acceptance_token,'response_format':self.response_format}
		r = requests.get("http://www.mediafire.com/api/user/accept_tos.php", params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Accepted the TOS succesfully"

	def get_content(self,content_type='files',order_by='name',order_direction='asc',chunk='1'): #Unfinished
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'content_type':content_type,'order_by':order_by,'order_direction':order_direction,'chunk':chunk}
	 	r = requests.get("http://www.mediafire.com/api/folder/get_content.php", params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			if (content_type == 'files'):
				return json['folder_content']['files']

			else:
				return json['folder_content']['folders']

	def file_get_info(self,quick_key):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':quick_key}
		r = requests.get("http://www.mediafire.com/api/file/get_info.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			return json['file_info']

	def file_delete(self,quick_key):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':quick_key}
		r = requests.get("http://www.mediafire.com/api/file/delete.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Deleted " + quick_key

	def file_move(self,quick_key,folder_key=''):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':quick_key,'folder_key':folder_key}
		r = requests.get("http://www.mediafire.com/api/file/move.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Moved " + quick_key + " to " + folder_key



mediafire = Mediafire(email,password,application_id,api_key,response_format)
mediafire.get_session_token()
