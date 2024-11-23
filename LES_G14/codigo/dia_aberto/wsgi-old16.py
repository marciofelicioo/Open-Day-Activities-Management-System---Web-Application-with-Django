
activate_this = 'C:/inetpub/wwwroot/DAUALG/grupo1_6/env/Scripts/activate_this.py'


# execfile(activate_this, dict(__file__=activate_this))


exec(open(activate_this).read(),dict(__file__=activate_this))




import os


import sys


import site




# Add the site-packages of the chosen virtualenv to work with


site.addsitedir('C:/inetpub/wwwroot/DAUALG/grupo1_6/env/Lib/site-packages')




# Add the app's directory to the PYTHONPATH


sys.path.append('C:/inetpub/wwwroot/DAUALG/grupo1_6')


sys.path.append('C:/inetpub/wwwroot/DAUALG/grupo1_6/dia_aberto')




os.environ['DJANGO_SETTINGS_MODULE'] = 'dia_aberto.settings'


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dia_aberto.settings")




from django.core.wsgi import get_wsgi_application


application = get_wsgi_application()
