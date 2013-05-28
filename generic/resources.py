class ResouceGetMixin(object):
    url = None
    context_object_name = None

    def get_headers(self):
        return {
            'authorization': self.request.session.get('tsuru_token'),
        }
