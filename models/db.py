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
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


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

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)                                                                                                             
#db=DAL("sqlite://recepies.sqlite")

db.auth_user.password.requires=IS_STRONG(min=8,upper=2,special=2)

#sets required fopr profile
gender=['Male', 'Female']
occupation_type=['Job', 'Buissness', 'Freelancer', 'Student', 'Activist', 'Other']
education=['PhD', 'Post-Graduate', 'Graduate', 'Senior Secondary', 'Secondary', 'Uneducated']
states=['Rajasthan']
caste_type=['Marwari', 'Mali']
marital_status=['Unmarried', 'Married', 'Divorced', 'Widow/Widower']
complexion=['Fair', 'Wheatish', 'Dark']

db.define_table('profile',
               Field('name','string',required=True),
               Field('user_id', 'reference auth_user', unique=True, default=auth.user_id or None, writable=False),
               Field('gender', 'string', required=True, requires=IS_IN_SET(gender)),
               Field('image7', 'upload', required=True),
                Field('image17', 'upload'),
                Field('image27', 'upload'),
                Field('image37', 'upload'),
                Field('dob7', 'datetime', required=True),
                Field('placebirth7', 'string'),
                Field('age7', 'integer', writable=False, default=0),
                Field('biodata7', 'upload'),
                Field('income7', 'integer', required=True, writable=True, default=45),
                Field('occupation_type7', 'string', required=True, requires=IS_IN_SET(occupation_type)),
                Field('occupation7', 'string'),
                Field('occupation_description7', 'text', length=400),
                Field('education7', 'string', required=True, requires=IS_IN_SET(education)),
                Field('education_description7', 'text', length=400),
                Field('complexion7', 'string', requires=IS_IN_SET(complexion)),
                Field('height7', 'string'),
                Field('weight7', 'integer'),
                Field('disability7', 'string'),
                Field('state_live7', requires=IS_IN_SET(states)),
                Field('address7', 'text', length=200),
                Field('phone_no7','string',length=10),
                Field('caste_type7', 'string', requires=IS_IN_SET(caste_type)),
                Field('caste7', 'string'),
                Field('gotra7', 'string'),
                Field('manglik7', 'boolean'),
                Field('mother_name7', 'string'),
                Field('mother_occupation7','string'),
                Field('father_name7', 'string'),
                Field('father_occupation7', 'string'),
                Field('sibling_no7', 'integer'),
                Field('marital_status7', 'string', required=True, requires=IS_IN_SET(marital_status)),
                Field('availability7', 'boolean', default=True, writable=False, readable=False),
                Field('pub_date7', 'datetime', default=request.now, writable=False, readable=False)
               )
