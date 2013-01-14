from Cert import Cert
import httplib
import json
from error import Error
from urlparse import urlparse
class Token(Error):
	
	def __init__(self):
		
		self.params = Cert().get_params()
		self.headers = Cert().get_headers()
		self.url = Cert().get_url()

		self.conn = httplib.HTTPConnection(self.url)
		self.conn.request("POST", "/v2.0/tokens", self.params, self.headers)
		self.response=self.conn.getresponse()
		self.token_metadata=self.response.read()
		self.token_metadata = json.loads(self.token_metadata)
		self.conn.close()
		self.apitoken = self.token_metadata['access']['token']['id']
		self.apiurl = self.token_metadata['access']['serviceCatalog'][0]['endpoints'][0]['publicURL']
		self.apiurlt = urlparse(self.apiurl)