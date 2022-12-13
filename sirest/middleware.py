from sirest.utils import execute_sql

class Authenticate(object):
    def __init__(this, get_response):
        this.get_response = get_response
    
    def __call__(this, request):
        session_id = request.COOKIES.get('session_id')
        if (session_id != None):
            request.email = execute_sql(f"select email from session where id = '{session_id}';")[0][0]
            print('middleware', request.email)
        return this.get_response(request)