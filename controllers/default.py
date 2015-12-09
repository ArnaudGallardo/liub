import math, os, json, uuid
from gluon.contrib.populate import populate

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
    print session.test
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


def test_populate():
    populate(db.grad,50)
    db.commit()

    return 'Done'


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
    form.element(_id='question_university')['_autocomplete']='off'
    if form.process(onvalidation=question_process).accepted:
        print form.vars
    return dict(form=form)


@auth.requires_membership('admin')
def admin():
    csv_to_dict()
    return dict(notif="Notif")

@auth.requires_signature()
def admin_data_univ():
    #Now I grab the universities data
    count = db.university.id.count()
    universities = db().select(db.university.approved, count, groupby=db.university.approved)
    uni = 0
    for row in universities:
        if row.university.approved == False:
            uni = row[count]
    #Now I grab the grads student profiles data
    count = db.grad.id.count()
    grads = db().select(db.grad.approved, count, groupby=db.grad.approved)
    grad = 0
    for row in grads:
        if row.grad.approved == False:
            grad = row[count]

    rows = db(db.university.approved==False).select(db.university.ALL, orderby=~db.university.created_on)
    d = [{'id':r.id,'name': r.name,'lat': r.lat,'lng':r.lng,'country':r.country,'info':r.info,'class':'danger'}
         for r in rows]
    rows = db(db.university.approved==True).select(db.university.ALL, orderby=~db.university.created_on)
    e = [{'id':r.id,'name': r.name,'lat': r.lat,'lng':r.lng,'country':r.country,'info':r.info,'class':'','approved':r.approved}
         for r in rows]
    f = [i+1 for i in range(0,((len(e)+len(d))/5)+1)]
    return response.json(dict(result=d,result_v=e,uni=uni,grad=grad,pages=f))

@auth.requires_signature()
def admin_validate_univ():
    db.university.update_or_insert((db.university.id == request.vars.id), approved=True)
    return 'ok'

@auth.requires_signature()
def admin_delete_univ():
    db(db.university.id == request.vars.id).delete()
    return 'ok'

@auth.requires_signature()
def admin_edit_univ():
    type = request.vars.type
    if type == 'lat':
        db.university.update_or_insert((db.university.id == request.vars.id), lat=request.vars.value)
    elif type == 'lng':
        db.university.update_or_insert((db.university.id == request.vars.id), lng=request.vars.value)
    elif type == 'country':
        db.university.update_or_insert((db.university.id == request.vars.id), country=request.vars.value)
    elif type == 'name':
        db.university.update_or_insert((db.university.id == request.vars.id), name=request.vars.value)
    elif type == 'info':
        db.university.update_or_insert((db.university.id == request.vars.id), info=request.vars.value)
    return "ok"


@auth.requires_signature()
def admin_validate_grad():
    db.grad.update_or_insert((db.grad.id == request.vars.id), approved=True)
    return 'ok'


@auth.requires_signature()
def admin_refuse_grad():
    db.grad.update_or_insert((db.grad.id == request.vars.id), refused=True, refused_message=request.vars.message)
    return 'ok'


@auth.requires_signature()
def admin_data_grad():
    #Now I grab the universities data
    count = db.university.id.count()
    universities = db().select(db.university.approved, count, groupby=db.university.approved)
    uni = 0
    for row in universities:
        if row.university.approved == False:
            uni = row[count]
    #Now I grab the grads student profiles data
    count = db.grad.id.count()
    grads = db().select(db.grad.approved, count, groupby=db.grad.approved)
    grad = 0
    for row in grads:
        if row.grad.approved == False:
            grad = row[count]

    rows = db(db.grad.approved==False).select(db.grad.ALL, orderby=~db.grad.modified_on)
    d = [{'id':r.id,'student': r.student.first_name+' '+r.student.last_name,'university': r.university.name,'link_blog':r.blog,
          'file_link':r.picture.file_link,'quote':r.yr_quote}
         for r in rows]
    f = [i+1 for i in range(0,(len(d)/5)+1)]
    return response.json(dict(result=d,uni=uni,grad=grad,pages=f))


@auth.requires_signature()
def admin_data():
    result = {}
    #First I grab the questions data
    year = json.loads(request.vars.year)
    count = db.question.id.count()
    questions = db(db.question.created_on.year() == year).select(db.question.created_on.month(), count, groupby=db.question.created_on.month())
    questions_label = db().select(db.question.created_on.year(), groupby=db.question.created_on.year())
    print questions
    print questions_label
    label = []
    for row in questions_label:
        label.append({'id':row['_extra']["web2py_extract('year',question.created_on)"],
                      'name':row['_extra']["web2py_extract('year',question.created_on)"]})
    result['questions_label'] = label
    data = [0,0,0,0,0,0,0,0,0,0,0,0]
    for row in questions:
        data[row['_extra']["web2py_extract('month',question.created_on)"]-1] = row[count]
    result['questions'] = data
    #Now I grab the students data
    count = db.auth_user.id.count()
    promos = db().select(db.auth_user.promotion, count, groupby=db.auth_user.promotion)
    result['students_label'] = []
    result['students_data'] = []
    for row in promos:
        result['students_label'].append(row.auth_user.promotion)
        result['students_data'].append(row[count])
    print promos
    #Now I grab the universities data
    count = db.university.id.count()
    universities = db().select(db.university.approved, count, groupby=db.university.approved)
    print universities
    data = [0,1]
    for row in universities:
        if row.university.approved:
            data[0] = row[count]
        elif row.university.approved == False:
            data[1] = row[count]
    result['universities'] = data
    #Now I grab the grads student profiles data
    count = db.grad.id.count()
    grads = db().select(db.grad.approved, count, groupby=db.grad.approved)
    print grads
    data = [0,1]
    for row in grads:
        if row.grad.approved:
            data[0] = row[count]
        elif row.grad.approved == False:
            data[1] = row[count]
    result['grads'] = data
    return response.json(result)


def test_upload():
    image_form = FORM(
        INPUT(_name='image_title',_type='text'),
        INPUT(_name='image_file',_type='file'))
    if image_form.accepts(request.vars,formname='image_form'):
        image = db.image.file_link.store(image_form.vars.image_file.file, image_form.vars.image_file.filename)
        id = db.image.insert(file_link=image,title=image_form.vars.image_title)
    images = db().select(db.image.ALL)
    return dict(images=images)


@auth.requires_signature()
def profile_edit():
    refused = False
    message = ""
    if (request.vars.univ == "" or request.vars.blog == "" or request.vars.quote == ""):
        refused=True
        message = "One of your answer is empty."
    uni_name = request.vars.univ
    row = db(db.university.name==uni_name).select(db.university.id)
    if not row:
        new_uni = db.university.insert(name=request.vars.univ)
        request.vars.univ = new_uni
    else:
        request.vars.univ = row.first()
    db.grad.update_or_insert((db.grad.student == auth.user.id), approved=False,
                             blog=request.vars.blog,
                             yr_quote=request.vars.quote,
                             university=request.vars.univ,
                             modified_on=datetime.utcnow(),
                             refused=refused,
                             refused_message=message)
    return 'ok'


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
    image_form = None
    user_data = {
        'id':'',
        'university':'',
        'link_blog':'',
        'file_link':'',
        'quote':'',
        'refused':False,
        'refused_message':''
    }
    if request.args(0)=='profile':
        image_form = FORM(
        INPUT(_name='image_title',_type='text'),
        INPUT(_name='image_file',_type='file'))
        if image_form.accepts(request.vars,formname='image_form'):
            if image_form.vars.image_file != "":
                if image_form.vars.image_title == "":
                   image_form.vars.image_title = "No title"
                image = db.image.file_link.store(image_form.vars.image_file.file, image_form.vars.image_file.filename)
                id = db.image.insert(file_link=image,title=image_form.vars.image_title)
                db.grad.update_or_insert((db.grad.student == auth.user.id), picture=id)
                redirect(URL('default','user', args=['profile']))
        rows = db(db.grad.student==auth.user.id).select(db.grad.ALL)
        d = [{'id':r.id,'university': r.university.name,'link_blog':r.blog,
              'file_link':r.picture.file_link,'quote':r.yr_quote,'refused':r.refused,'refused_message':r.refused_message} for r in rows]
        if d!=[]:
            if d[0]['university'] != None:
                user_data['university'] = d[0]['university']
            if d[0]['link_blog'] != None:
                user_data['link_blog'] = d[0]['link_blog']
            if d[0]['file_link'] != None:
                user_data['file_link'] = d[0]['file_link']
            if d[0]['quote'] != None:
                user_data['quote'] = d[0]['quote']
            if d[0]['id'] != None:
                user_data['id'] = d[0]['id']
            if d[0]['refused'] != None:
                user_data['refused'] = d[0]['refused']
            if d[0]['refused_message'] != None:
                user_data['refused_message'] = d[0]['refused_message']
    return dict(form=auth(),grad_data=user_data)


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


def link(): return response.download(request,db,attachment=False)


