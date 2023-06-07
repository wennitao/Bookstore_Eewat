import time

from fe.access import auth
from fe import conf

from be import serve

serve.be_run()

user_id = "test_register_user_{}".format(time.time())
password = "test_register_password_{}".format(time.time())
auth = auth.Auth(conf.URL)
code = auth.register(user_id, password)
print (code)
assert code == 200