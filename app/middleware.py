from django.utils.deprecation import MiddlewareMixin

class CustomSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            request.session.cookie_name = 'admin_sessionid'
        else:
            request.session.cookie_name = 'ecommerce_sessionid'
