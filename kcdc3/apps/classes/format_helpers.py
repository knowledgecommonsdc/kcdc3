"""Helpers for formatting text"""

# Provide website address; add http:// if no protocol is specified
def add_protocol(address):
	if "http://" in address or "https://" in address:
		return address
	else:
		address = "http://" + address
		return address

# Provide website with http:// removed
def remove_protocol(address):
	address = address.replace("http://","")
	address = address.replace("https://","")
	return address

