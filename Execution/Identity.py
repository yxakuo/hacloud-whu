import Token
import httplib
import Cert
import json
import urllib
from urlparse import urlparse

class List_User():
    token = Token.Token
    apitoken = token().get_apitoken()
    apiurl = token().get_apiurl()
    apiurlt = urlparse(apiurl)
    
    def list_user(self):
        params = '{}'
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        tenant_id = '70c6e018c0d9416ba85459884adeccd2'
        test= '/v2.0/70c6e018c0d9416ba85459884adeccd2'
        user_id='14c1ac745c804e79b2880f04fb232e2e'
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('GET','%s/users/%s'%(test,user_id),params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        print result
        result = json.loads(result)
        conn.close()
        return result

class List_Tenant():
    token = Token.Token
    apitoken = token().get_apitoken()
    apiurl = token().get_apiurl()
    apiurlt = urlparse(apiurl)
    
    def list_tenant(self):
        params = '{}'
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        tenant_id = '70c6e018c0d9416ba85459884adeccd2'
        test= '/v2.0/70c6e018c0d9416ba85459884adeccd2'
        user_id='14c1ac745c804e79b2880f04fb232e2e'
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('GET','%s/tenant'%test,params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        print result
        result = json.loads(result)
        conn.close()
        return result

class Add_User():
    token = Token.Token
    apitoken = token().get_apitoken()
    apiurl = token().get_apiurl()
    apiurlt = urlparse(apiurl)
    
    def add_user(self):
        params = {
                  "user": {
                           "username": "gzl-testuser",
                           "email": "john.smith@example.org",
                           "enabled": False,
                           "OS-KSADM:password": "guozilong"
                           }
                  }
        params = json.dumps(params)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }

        test= '/v2.0/70c6e018c0d9416ba85459884adeccd2'
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('POST','%s/users'%test,params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        print result
        result = json.loads(result)
        conn.close()
        return result

add = Add_User
add().add_user()