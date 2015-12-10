# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
from datetime import datetime
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

#GLOBAL VARIABLES
YEAR = 2015
TYPES = ['Documents','Classes','Campus Life','Other']
MAJOR = ["CS","PHY","CHY","MATH","BIO","MCS","PC"]
MAJOR_LG = ["Computer Science","Physics","Chemistry","Mathematics","Biology","Math/CS","Phys/Chem"]
MAJOR_OPTIONS = [OPTION(MAJOR_LG[i],_value=MAJOR[i]) for i in range(0,len(MAJOR))]

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

#########################################################################
#CUSTOM TABLE AND VALIDATION BRAH
#########################################################################
db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128, default='',writable=False),
    Field('last_name', length=128, default='',writable=False),
    Field('email', length=128, default='', unique=True), # required
    Field('password', 'password', length=512,            # required
          readable=False, label='Password'),
    Field('promotion','integer',writable=False),
    Field('major'),
    Field('registration_key', length=512,                # required
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,              # required
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,                 # required
          writable=False, readable=False, default=''))

## do not forget validators
custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [CRYPT()]
custom_auth_table.promotion.requires = IS_IN_SET([2013,2014,2015]) #DONT FORGET TO REMOVE
custom_auth_table.major.requires = IS_IN_SET(MAJOR)
custom_auth_table.email.requires = [
  IS_EMAIL(error_message=auth.messages.invalid_email),
  IS_NOT_IN_DB(db, custom_auth_table.email)]

auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table
auth.settings.create_user_groups = None
auth.settings.everybody_group_id = 2

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
def widget(**kwargs):
    return lambda field, value, kwargs=kwargs: SQLFORM.widgets[field.type].widget(field, value, **kwargs)

db.define_table('image',
                Field('title'),
                Field('file_link', 'upload'),
                format = '%(title)s')

db.define_table('university',
                Field('name'),
                Field('lat', 'double'),
                Field('lng', 'double'),
                Field('country'),
                Field('info', 'text'),
                Field('created_on','datetime'),
                Field('approved', 'boolean', writable=False, readable=False)
                )
db.university.created_on.default = datetime.utcnow()
db.university.approved.default = False

db.define_table('grad',
                Field('student', db.auth_user, writable=False, readable=False, unique=True),
                Field('university', 'reference university'),
                Field('blog'),
                Field('yr_quote', 'text'),
                Field('picture','reference image'),
                Field('approved', 'boolean', writable=False, readable=False),
                Field('modified_on','datetime', writable=False, readable=False),
                Field('refused', 'boolean', writable=False, readable=False),
                Field('refused_message','text', writable=False, readable=False)
                )
db.grad.refused.default = False
db.grad.approved.default = False
db.grad.picture.default = 1
db.grad.modified_on.default = datetime.utcnow()

db.define_table('question',
                Field('author', db.auth_user, writable=False, readable=False),
                Field('university', 'reference university'),
                Field('title', widget=widget(_placeholder='Titre', _style='width:75%')),
                Field('ques_content', 'text'),
                Field('created_on','datetime', writable=False, readable=False),
                Field('keywords','list:string'),
                Field('content_type', widget=widget(_placeholder='Type')),
                Field('done', 'boolean'),
                )
db.question.content_type.requires = IS_IN_SET(TYPES)
db.question.author.default = auth.user_id
db.question.created_on.default = datetime.utcnow()
db.question.done.default = False

db.define_table('answer',
                Field('question','reference question'),
                Field('author', db.auth_user, writable=False, readable=False),
                Field('answer_content', 'text'),
                Field('posted_on','datetime', writable=False, readable=False),
                Field('good', 'boolean'),
                Field('is_backup','boolean'),
                Field('edited','boolean')
                )
db.answer.author.default = auth.user_id
db.answer.posted_on.default = datetime.utcnow()
db.answer.good.default = False
db.answer.edited.default = False

#TIMEZONE
is_timezone_unknown = (session.user_timezone is None)
user_timezone = session.user_timezone or 'UTC'


# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)


######################
# Logging
import logging, sys
FORMAT = "%(asctime)s %(levelname)s %(process)s %(thread)s %(funcName)s():%(lineno)d %(message)s"
logging.basicConfig(stream=sys.stderr)
logger = logging.getLogger(request.application)
logger.setLevel(logging.INFO)

# Let's log the request.
logger.info("====> Request: %r %r %r %r" % (request.env.request_method, request.env.path_info, request.args, request.vars))
