class Cert():
    params = '{"auth":{"tenantName":"admin", "passwordCredentials":{"username":"admin", "password": "admin"}}}'
    headers = {"Content-Type": "application/json"}
    url = '127.0.0.1:5000'
    def get_url(self):
        return self.url
    def get_headers(self):
        return self.headers
    def get_params(self):
        return self.params
    def set_url(self,url):
        self.url = url
        return self.url
    def set_headers(self,headers):
        self.headers = headers
        return headers
    def set_params(self,params):
        self.params = params
        return params