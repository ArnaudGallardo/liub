# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(IMG(_src=URL('static', 'images/logo.png'),
                      _height="45px", _title="LIUB"), _class="brand",_href=URL('default','search'))
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################
if request.function == 'admin':
    response.menu = [
        (T('Search'), (request.function=='search'), URL('default', 'search'), []),
        (XML(T('New ')+I(_class='fa fa-university')+' '+str(SPAN('',_class='badge',_id='uni_notif')), sanitize=False), ((request.function=='admin') & (request.args(0) == 'university')), URL('default', 'admin',args=['university']), []),
        (XML(T('New ')+I(_class='fa fa-graduation-cap')+' '+str(SPAN('',_class='badge',_id='grad_notif')), sanitize=False), ((request.function=='admin') & (request.args(0) == 'student')), URL('default', 'admin',args=['student']), []),
    ]
else:
    response.menu = [
        (T('Search'), (request.function=='search'), URL('default', 'search'), []),
        (T('Ask Question'), (request.function=='ask'), URL('default', 'ask'), []),
    ]

DEVELOPMENT_MENU = False

def get_lang_switch(language):
    if (language == 'fr'):
        return 'english'
    return 'français'

def user_bar():
    action = URL('default','user');
    bar = None
    if auth.user:
        text_head = T('Logged as') + ' ' + auth.user.first_name + ' ' + auth.user.last_name
        text_logout = I(_class='fa fa-sign-out') + ' ' + T('logout')
        text_profile = I(_class='fa fa-user') + ' ' + T('profile')
        text_admin = I(_class='fa fa-gears') + ' ' + T('administration page')
        text_language = I(_class='fa fa-language') + ' ' + T('changer pour') + ' ' + get_lang_switch(session.language)
        head = LI(text_head,_class='dropdown-header')
        lang = A(text_language, _href='#', _id='lang')
        logout = A(text_logout, _href=action+'/logout')
        admin=None
        if (auth.has_membership(1,auth.user_id)):
            admin = A(text_admin,_href=URL('default','admin'))
        profile = A(text_profile, _href=action+'/profile')
        button = BUTTON(I(_class='fa fa-cog'),_class='btn btn-default dropdown-toggle', _type='button',_id='profileMenu'
                        , **{'_data-toggle': 'dropdown'
                                ,'_aria-haspopup': 'true', '_aria-expanded': 'false'})
        ul = UL(head,lang,profile,logout,admin,_class='dropdown-menu')
        bar = DIV(button,ul,_class='dropdown')

    return bar

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
          (T('This App'), False, '#', [
              (T('Design'), False, URL('admin', 'default', 'design/%s' % app)),
              LI(_class="divider"),
              (T('Controller'), False,
               URL(
               'admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
              (T('View'), False,
               URL(
               'admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
              (T('DB Model'), False,
               URL(
               'admin', 'default', 'edit/%s/models/db.py' % app)),
              (T('Menu Model'), False,
               URL(
               'admin', 'default', 'edit/%s/models/menu.py' % app)),
              (T('Config.ini'), False,
               URL(
               'admin', 'default', 'edit/%s/private/appconfig.ini' % app)),
              (T('Layout'), False,
               URL(
               'admin', 'default', 'edit/%s/views/layout.html' % app)),
              (T('Stylesheet'), False,
               URL(
               'admin', 'default', 'edit/%s/static/css/web2py-bootstrap3.css' % app)),
              (T('Database'), False, URL(app, 'appadmin', 'index')),
              (T('Errors'), False, URL(
               'admin', 'default', 'errors/' + app)),
              (T('About'), False, URL(
               'admin', 'default', 'about/' + app)),
              ]),
          ('web2py.com', False, '#', [
             (T('Download'), False,
              'http://www.web2py.com/examples/default/download'),
             (T('Support'), False,
              'http://www.web2py.com/examples/default/support'),
             (T('Demo'), False, 'http://web2py.com/demo_admin'),
             (T('Quick Examples'), False,
              'http://web2py.com/examples/default/examples'),
             (T('FAQ'), False, 'http://web2py.com/AlterEgo'),
             (T('Videos'), False,
              'http://www.web2py.com/examples/default/videos/'),
             (T('Free Applications'),
              False, 'http://web2py.com/appliances'),
             (T('Plugins'), False, 'http://web2py.com/plugins'),
             (T('Recipes'), False, 'http://web2pyslices.com/'),
             ]),
          (T('Documentation'), False, '#', [
             (T('Online book'), False, 'http://www.web2py.com/book'),
             LI(_class="divider"),
             (T('Preface'), False,
              'http://www.web2py.com/book/default/chapter/00'),
             (T('Introduction'), False,
              'http://www.web2py.com/book/default/chapter/01'),
             (T('Python'), False,
              'http://www.web2py.com/book/default/chapter/02'),
             (T('Overview'), False,
              'http://www.web2py.com/book/default/chapter/03'),
             (T('The Core'), False,
              'http://www.web2py.com/book/default/chapter/04'),
             (T('The Views'), False,
              'http://www.web2py.com/book/default/chapter/05'),
             (T('Database'), False,
              'http://www.web2py.com/book/default/chapter/06'),
             (T('Forms and Validators'), False,
              'http://www.web2py.com/book/default/chapter/07'),
             (T('Email and SMS'), False,
              'http://www.web2py.com/book/default/chapter/08'),
             (T('Access Control'), False,
              'http://www.web2py.com/book/default/chapter/09'),
             (T('Services'), False,
              'http://www.web2py.com/book/default/chapter/10'),
             (T('Ajax Recipes'), False,
              'http://www.web2py.com/book/default/chapter/11'),
             (T('Components and Plugins'), False,
              'http://www.web2py.com/book/default/chapter/12'),
             (T('Deployment Recipes'), False,
              'http://www.web2py.com/book/default/chapter/13'),
             (T('Other Recipes'), False,
              'http://www.web2py.com/book/default/chapter/14'),
             (T('Helping web2py'), False,
              'http://www.web2py.com/book/default/chapter/15'),
             (T("Buy web2py's book"), False,
              'http://stores.lulu.com/web2py'),
             ]),
          (T('Community'), False, None, [
             (T('Groups'), False,
              'http://www.web2py.com/examples/default/usergroups'),
              (T('Twitter'), False, 'http://twitter.com/web2py'),
              (T('Live Chat'), False,
               'http://webchat.freenode.net/?channels=web2py'),
              ]),
        ]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu() 
