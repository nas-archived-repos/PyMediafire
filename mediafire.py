import requests,hashlib,json
email =""
password = ""
application_id = ""
api_key = ""

class Mediafire_User:
	def __init__(self,email,password,application_id,api_key):
		self.email = email
		self.password = password
		self.application_id = application_id
		self.api_key = api_key
		self.response_format = 'json'
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
			return json['session_token']

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

	def get_content(self,content_type='files',folder_key='',order_by='name',order_direction='asc',chunk='1'): #Unfinished
		parameters = {'session_token':self.session_token,'folder_key':folder_key,'response_format':self.response_format,'content_type':content_type,'order_by':order_by,'order_direction':order_direction,'chunk':chunk}
	 	r = requests.get("http://www.mediafire.com/api/folder/get_content.php", params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			if (content_type == 'files'):
				files = []
				for x in json['folder_content']['files']:
					file = Mediafire_File(self.session_token,x['quickkey'])
					files.append(file)
				return files				
			else:
				folders = []
				for x in json['folder_content']['folders']:
					folder = Mediafire_Folder(self.session_token,x['folderkey'])
					folders.append(folder)
				return folders
				 
	def folder_create(self,foldername,parent_key=''):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'foldername':foldername,'parent_key':parent_key}
		r = requests.get("http://www.mediafire.com/api/folder/create.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			return Mediafire_Folder(self.session_token,json['folder_key'])





class Mediafire_File:
	def __init__(self,session_token,quick_key):
		self.quick_key = quick_key
		self.response_format = 'json'
		self.session_token = session_token

	def get_info(self):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key}
		r = requests.get("http://www.mediafire.com/api/file/get_info.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			return json['file_info']

	def delete(self):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key}
		r = requests.get("http://www.mediafire.com/api/file/delete.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Deleted " + self.quick_key

	def move(self,folder_key=''):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'folder_key':folder_key}
		r = requests.get("http://www.mediafire.com/api/file/move.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Moved " + self.quick_key + " to " + folder_key

	def update(self,filename,description,tags,privacy,note_subject,note_description):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'filename':filename,'description':description,'tags':tags,'privacy':privacy,'note_subject':note_subject,'note_description':note_description}
		r = requests.get("http://www.mediafire.com/api/file/update.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Changed the info for " + self.quick_key

	def update_password(self,password=""):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'password':password}
		r = requests.get("http://www.mediafire.com/api/file/update_password.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Changed the password for " + self.quick_key

	def update_file(self,to_quickkey):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'from_quickkey':self.quick_key,'to_quickkey':to_quickkey}
		r = requests.get("http://www.mediafire.com/api/file/update_file.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Update the quickkey for " + self.quick_key +" to " + to_quickkey
			self.quick_key = to_quickkey

	def copy(self,folder_key=''):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'folder_key':folder_key}
		r = requests.get("http://www.mediafire.com/api/file/copy.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Copied " + self.quick_key +" to " + folder_key
			return json['new_quickkeys']

	def get_links(self,link_type=''):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'link_type':link_type}
		r = requests.get("http://www.mediafire.com/api/file/get_links.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			return json['links']

	def collaborate(self,emails='',duration='',message='',public='no',email_notification='no'):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'emails':emails,'duration':duration,'message':message,'public':public,'email_notification':email_notification}
		r = requests.get("http://www.mediafire.com/api/file/collaborate.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			return json['collaboration_links'][0]['link']

	def one_time_download(self,get_counts_only='no',duration='',email_notification='no',burn_after_use='yes',success_callback_url='',error_calback_url='',bind_ip=''):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'quick_key':self.quick_key,'get_counts_only':get_counts_only,'duration':duration,'email_notification':email_notification,'success_callback_url':success_callback_url,'error_calback_url':error_calback_url,'bind_ip':bind_ip,'burn_after_use':burn_after_use}
		r = requests.get("http://www.mediafire.com/api/file/one_time_download.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			return {'link':json['one_time_download'],'token':json['token']}

	def configure_one_time_download(self,token,duration='',email_notification='no',burn_after_use='yes',success_callback_url='',error_calback_url='',bind_ip=''): #Doesn't work for some reason
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'token':token,'duration':duration,'email_notification':email_notification,'success_callback_url':success_callback_url,'error_calback_url':error_calback_url,'bind_ip':bind_ip,'burn_after_use':burn_after_use}
		r = requests.get("http://www.mediafire.com/api/file/configure_one_time_download.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Succesfully changed the " + token + " one time download"

class Mediafire_Folder:
	def __init__(self,session_token,folder_key):
		self.folder_key = folder_key
		self.response_format = 'json'
		self.session_token = session_token

	def get_info(self):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key}
		r = requests.get("http://www.mediafire.com/api/folder/get_info.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			return json['folder_info']

	def delete(self):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key}
		r = requests.get("http://www.mediafire.com/api/folder/delete.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Deleted " + self.folder_key

	def move(self,folder_key_dst=''):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key_src':self.folder_key,'folder_key_dst':folder_key_dst}
		r = requests.get("http://www.mediafire.com/api/folder/move.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Moved " + self.folder_key +" to " + folder_key_dst

	def update(self,foldername='',description='',tags='',privacy='',privacy_recursive='',note_subject='',note_description=''):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key,'foldername':foldername,'description':description,'tags':tags,'privacy':privacy,'privacy_recursive':privacy_recursive,'note_subject':note_subject,'note_description':note_description}
		r = requests.get("http://www.mediafire.com/api/folder/update.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print "Updated " + foldername
			

	def attach_foreign(self): #Not tested
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key}
		r = requests.get("http://www.mediafire.com/api/folder/attach_foreign.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print 'Succesfully attached ' + self.folder_key

	def detach_foreign(self): #Not tested
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':folder_key}
		r = requests.get("http://www.mediafire.com/api/folder/detach_foreign.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print 'Succesfully detached ' + self.folder_key

	def get_depth(self):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key}
		r = requests.get("http://www.mediafire.com/api/folder/get_depth.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print json['folder_depth']
			return json['folder_depth']['depth']

	def get_siblings(self,content_filter='all',start='',limit=''): #Don't know what this does
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key,'content_filter':content_filter,'start':start,'limit':limit}
		r = requests.get("http://www.mediafire.com/api/folder/get_siblings.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print json

	def search(self,search_text):
		parameters = {'session_token':self.session_token,'response_format':self.response_format,'folder_key':self.folder_key,'search_text':search_text}
		r = requests.get("http://www.mediafire.com/api/folder/search.php",params = parameters)
		json = r.json()['response']
		if (json['result'] == 'Error'):
			print json['message']
		else:
			print json['results']
			return json['results']


