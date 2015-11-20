import math
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


def convert_pos(lat, long):
    longitude_shift = 0
    x_pos = 0
    y_pos = 0
    map_width = 1652
    map_height = 1221

    x = (map_width * (180 + long) / 360) % map_width + longitude_shift
    lat = lat * math.pi / 180
    y = math.log(math.tan((lat/2) + (math.pi/4)))
    y = (map_height / 2) - (map_width * y / (2 * math.pi)) + y_pos

    x -= x_pos - 20
    y -= y_pos + 72

    print x,':',y

@auth.requires_login()
def search():
    convert_pos(35,139.4)
    if request.args(0)=='advice':
        print 'advice'
    elif request.args(0)=='user':
        print 'user'
    elif request.args(0)=='university':
        print 'university'
    return dict(message=T('Search Page'))


@auth.requires_signature()
def lang():
    lang = request.vars.lang
    if (lang is None) or (lang == 'fr'):
        session.language = 'en'
    else:
        session.language = 'fr'
    return "ok"


def universities():
    data = db().select(db.university.ALL)
    return response.json({'places': data})


def add_university():
    form = SQLFORM(db.university)
    if form.process().accepted:
        session.flash = T('The data was inserted')
        redirect(URL('default', 'index'))
    return dict(form=form)


def ask():
    form = SQLFORM(db.question)
    if form.process().accepted:
        session.flash = T('The data was inserted')
        redirect(URL('default', 'index'))
    return dict(form=form)


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


