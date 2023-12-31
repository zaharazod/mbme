import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'awa.settings')

application = get_wsgi_application()

# Determines if WSGI is running in embedded/daemon mode
# def application(environ, start_response):
#     status = '200 OK'

#     if not environ['mod_wsgi.process_group']:
#         output = u'EMBEDDED MODE'
#     else:
#         output = u'DAEMON MODE'

#     response_headers = [('Content-Type', 'text/plain'),
#                         ('Content-Length', str(len(output)))]

#     start_response(status, response_headers)

#     return [output.encode('UTF-8')]
