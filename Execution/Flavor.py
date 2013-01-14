import Token
import httplib
import json
import urllib
from urlparse import urlparse
from Token import Token
class Flavor(Token):
    
    def __init__(self):
        Token.__init__(self)
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request("GET", "%s/flavors/detail?" %self.apiurlt[2], params, headers)
        response = conn.getresponse()
        self.flavor_metadata = response.read()
        self.flavor_metadata = json.loads(self.flavor_metadata)
        conn.close()
        
    def Get_AllFlavorHref(self):
        m=range(len(self.flavor_metadata['flavors']))
        flavor_href={}
        for i in m:
            flavor_href[i]=self.flavor_metadata['flavors'][i]['links'][0]['href']
        return flavor_href
    
    def Get_SpecificFlavorHref(self,flavor_id):
        m=range(len(self.flavor_metadata['flavors']))
        flavor_href=''
        for i in m:
            if self.flavor_metadata['flavors'][i]['id'] == flavor_id:
                flavor_href = self.flavor_metadata['flavors'][i]['links'][0]['href']
                return flavor_href
            
    def Create_Flavor(self,flavor_attributes):
        params = json.dumps(flavor_attributes)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request("POST", "%s/flavors" %self.apiurlt[2], params, headers)
        response = conn.getresponse()
        flavor_metadata = response.read()
        flavor_metadata = json.loads(flavor_metadata)
        conn.close()
        return flavor_metadata