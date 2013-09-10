from mediafire import Mediafire_User
#Replace blanks with appropriate data 
email =""
password = ""
application_id = ""
api_key = ""


test_user = mediafire.Mediafire_User(email,password,application_id,api_key)
test_user.get_session_token()
