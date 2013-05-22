import socket

if socket.gethostname() == "knowledgecommonsdc":
	from prod import *
else:
	from dev import *
