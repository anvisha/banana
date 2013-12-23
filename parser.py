#This is the parser to handle SMS requests.
import re

def sms_parser(text):
	print text
	for m in re.finditer("(\d+) (\w+)", text):
		user_phone = m.group(1)
		contact = m.group(2)
		return (user_phone, contact)
	return False


