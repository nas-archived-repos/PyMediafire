from mediafire.mediafire_user import Mediafire_User

email =""
password = ""
application_id = ""
api_key = ""


test_user = Mediafire_User(email,password,application_id,api_key)
test_user.get_session_token()
print(test_user.get_content()[0].get_info())