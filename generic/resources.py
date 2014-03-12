class ResouceGetMixin(object):
    url = None
    context_object_name = None

    def get_headers(self):
        return {
            'authorization': self.request.session.get('tsuru_token'),
        }

#     def tsuru_request(self, method, url, data=None):
#     	response = requests.request(method, url, data=data,
# 									headers=self.get_headers())
#     	if resp.status_code == 401
# 		    return redirect('/auth/login')
# 		return response


# requests.request("DELETE", "url")
# requests.request("POST", "url", data={"abc": 1}, headers=)
