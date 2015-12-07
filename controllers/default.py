import math, os

# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


@auth.requires_login()
def search():
    style = None
    content = None
    if request.args(0)=='advice':
        content = db().select(db.question.ALL)
        print 'advice'
    elif request.args(0)=='user':
        print 'user'
    elif request.args(0)=='university':
        style = open(os.path.join(request.folder, 'static', 'json', 'style.json'), 'rb').read()
        print 'university'
    return dict(message=T('Search Page'),style=style, content=content)


@auth.requires_signature()
def lang():
    lang = request.vars.lang
    if (lang is None) or (lang == 'fr'):
        session.language = 'en'
    else:
        session.language = 'fr'
    return "ok"


#@auth.requires_signature()
def universities():
    data = None
    if request.args(0)=='maps':
        result = db().select(db.university.id,db.university.lat,db.university.lng,db.university.name,db.university.country,db.university.info)
        result = {'places' : result}
    elif request.args(0)=='names':
        result = db().select(db.university.name,db.university.id)
    return response.json(result)


@auth.requires_login()
def add_university():
    form = SQLFORM(db.university)
    if form.process().accepted:
        session.flash = T('The data was inserted')
        redirect(URL('default', 'index'))
    return dict(form=form)


def question_process(form):
    uni_name = form.vars.university
    row = db(db.university.name==uni_name).select(db.university.id)
    if not row:
        new_uni = db.university.insert(name=form.vars.university)
        form.vars.university = new_uni
    else:
        form.vars.university = row.first()


@auth.requires_login()
def ask():
    form = SQLFORM(db.question)
    form.element(_id='question_university')['_placeholder']='University'
    form.element(_id='question_university')['_data-provide']='typeahead'
    if form.process(onvalidation=question_process).accepted:
        print form.vars
    return dict(form=form)

@auth.requires_membership('admin')
def admin():
    csv_to_dict()
    return 'lol'


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


