import math, os, json, uuid, pretty
from dateutil import tz
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
    promos_list = []
    nb_notif = 0
    if request.args(0)=='advice':
        print 'advice'
    elif request.args(0)=='student':
        promos = db().select(db.auth_user.promotion, groupby=db.auth_user.promotion)
        for p in promos:
            promos_list.append(p.promotion)
        print 'student'
    elif request.args(0)=='university':
        style = open(os.path.join(request.folder, 'static', 'json', 'style.json'), 'rb').read()
        print 'university'
    elif request.args(0) is None:
        l_visit = db(db.auth_user.id == auth.user_id).select(db.auth_user.last_visit).first().last_visit
        print l_visit
        if l_visit is None:
            l_visit = datetime(1990,1,1)
        result = db(db.question.created_on > l_visit).select(db.question.id)
        nb_notif = len(result)
    return dict(message=T('Search Page'),style=style,promos_list=promos_list,nb_notif=nb_notif)


@auth.requires_login()
def answer():
    if request.args(0) is None:
        redirect(URL('default','search',args=['advice']))
    brouillon = db((db.answer.author == auth.user_id) & (db.answer.is_backup == True)
                   & (db.answer.question == request.args(0))).select(db.answer.answer_content).first()
    if brouillon is not None:
        brouillon = brouillon.answer_content
    else:
        brouillon = ""
    return dict(brouillon=brouillon)


@auth.requires_signature()
def post_answer():
    backup = json.loads(request.vars.backup)
    content = request.vars.answer_content
    qid = request.vars.q_id
    print backup
    if backup:
        print 'update'
        db.answer.update_or_insert(((db.answer.author == auth.user_id) & (db.answer.is_backup == True) & (db.answer.question == qid)),
                                   question=qid,answer_content=content, is_backup=True)
    else:
        print 'answer'
        db.answer.update_or_insert(((db.answer.author == auth.user_id) & (db.answer.is_backup == True) & (db.answer.question == qid)),
                                   question=qid,answer_content=content, is_backup=False,posted_on=datetime.utcnow())
    return 'ok'


@auth.requires_signature()
def edit_answer():
    id = request.vars.id
    content = request.vars.content
    print content
    db.answer.update_or_insert((db.answer.id == id),answer_content=content,edited=True,posted_on=datetime.utcnow())
    return 'ok'


@auth.requires_signature()
def switch_good():
    id = request.vars.id
    qid = db(db.answer.id == id).select(db.answer.question).first().question
    good = db(db.answer.id == id).select(db.answer.good).first().good
    db.answer.update_or_insert((db.answer.id == id),good=not good)

    #Now we update the question 'done' status
    count = db.answer.id.count()
    good_answers = db(db.answer.question == qid).select(db.answer.good, count, groupby=db.answer.good)
    nb = 0
    for row in good_answers:
        if row.answer.good == True:
            nb = row[count]
    db.question.update_or_insert((db.question.id == qid),done=nb >= 1)
    return 'ok'


@auth.requires_signature()
def delete_answer():
    id = request.vars.id
    db(db.answer.id == id).delete()
    return 'ok'


@auth.requires_signature()
def answers_data():
    q_id = request.vars.question_id
    result = db(db.question.id == q_id).select(db.question.ALL).first()
    q_data = {
        'author':result.author.first_name+' '+result.author.last_name,
        'date':pretty.date(change_tz(result.created_on)),
        'content':str(XML(result.ques_content)),
        'title':result.title,
        'done':result.done
    }
    results = db((db.answer.question == q_id)&(db.answer.is_backup == False)).select(db.answer.ALL,orderby=db.answer.posted_on)
    a_data = [{'id':r.id,'author': r.author.first_name+' '+r.author.last_name, 'good':r.good,'edited':r.edited,
               'is_question_author':auth.user_id==r.question.author,'is_post_author':auth.user_id==r.author,
               'content':str(XML(r.answer_content)),'date':pretty.date(change_tz(r.posted_on))}
              for r in results]
    return response.json(dict(q_data=q_data,a_data=a_data))

def change_tz(date):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(session.user_timezone)
    date = date.replace(tzinfo=from_zone)
    date = date.astimezone(to_zone)
    date = datetime(date.year,date.month,date.day,date.hour,date.minute,date.second,date.microsecond)
    return date


@auth.requires_signature()
def question_data():
    db.auth_user.update_or_insert((db.auth_user.id == auth.user_id),last_visit=datetime.utcnow())
    univ = request.vars['search_data[univ]']
    type = request.vars['search_data[type]']
    content = request.vars['search_data[content]']
    major = request.vars['search_data[major]']
    q_univ = True
    if univ != "":
        univ_id = db(db.university.name==univ).select(db.university.id).first()
        q_univ = db.question.university == univ_id
    q_type = True
    if type != "" and type != "All":
        q_type = db.question.content_type == type
    q_content = True
    if content != "":
        q_content = db.question.ques_content == content
    q_major = True
    if major != "" and major != "All":
        db_students = db(db.auth_user.major == major).select(db.auth_user.id)
        li_students = []
        for s in db_students:
            li_students.append(s.id)
        print li_students
        q_major = db.question.author.belongs(li_students)
    q_content = True
    if content != "":
        q_content = False
        for word in content.split():
            q_content |= db.question.keywords.contains(word)
            q_content |= db.question.title.contains(word)
            q_content |= db.question.ques_content.contains(word)

    query = q_univ
    query &= q_type
    query &= q_major
    query &= q_content

    results = db(query).select(db.question.ALL,orderby=~db.question.created_on)
    d = [{'id':r.id,'done': r.done,'icon': str(get_icon(r.content_type)),'title':r.title,
          'university':r.university.name,'content':str(XML(r.ques_content)),'keywords':r.keywords,
          'author':r.author.first_name+' '+r.author.last_name,'date':pretty.date(change_tz(r.created_on))}
         for r in results]
    for f in d:
        nb_answer = db(db.answer.question == f['id']).select(db.answer.id)
        f['nb_answer'] = len(nb_answer)
    return response.json(d)


@auth.requires_signature()
def student_data():
    univ = request.vars['search_data[univ]']
    promo = request.vars['search_data[promo]']
    major = request.vars['search_data[major]']
    q_univ = True
    if univ != "":
        univ_id = db(db.university.name==univ).select(db.university.id).first()
        if univ_id is not None:
            db_univ = db(db.grad.university == univ_id.id).select(db.grad.student)
            li_students = []
            for s in db_univ:
                li_students.append(s.student)
            q_univ = db.auth_user.id.belongs(li_students)
    q_promo = True
    if promo != "" and promo != "All":
        q_promo = db.auth_user.promotion == promo
    q_major = True
    if major != "" and major != "All":
        q_promo = db.auth_user.major == major

    query = q_univ
    query &= q_promo
    query &= q_major

    results = db(query).select(db.auth_user.ALL,orderby=db.auth_user.last_name)
    d = []
    for r in results:
        d.append({'id':r.id,'data':{'name': r.first_name+' '+r.last_name,'email': r.email,'promo':r.promotion,
                  'major':get_lg_major(r.major)}})

    for s in d:
        r = db(db.grad.student == s['id']).select(db.grad.ALL).first()
        if r is not None:
            s['data']['university'] = r.university.name
            s['data']['blog'] = r.blog
            s['data']['quote'] = r.yr_quote
            s['data']['picture'] = r.picture.file_link
        else:
            s['data']['university'] = ""
            s['data']['blog'] = ""
            s['data']['quote'] = ""
            s['data']['picture'] = db(db.image.id == 1).select(db.image.file_link).first().file_link
    f = [i+1 for i in range(0,(len(d)/10)+1)]
    final_result = {'data':d,'pages':f}
    return response.json(final_result)


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
        redirect(URL('default','search',args=['advice']))
    return dict(form=form)

@auth.requires_signature()
def get_notif_data():
    query = db.grad.approved==False
    query &= db.grad.refused==False

    #Now I grab the universities data
    count = db.university.id.count()
    universities = db().select(db.university.approved, count, groupby=db.university.approved)
    uni = 0
    for row in universities:
        if row.university.approved == False:
            uni = row[count]
    #Now I grab the grads student profiles data
    count = db.grad.id.count()
    grads = db(query).select(db.grad.approved, count, groupby=db.grad.approved)
    grad = 0
    for row in grads:
        if row.grad.approved == False:
            grad = row[count]
    return response.json(dict(uni=uni,grad=grad))

@auth.requires_membership('admin')
def admin():
    csv_to_dict()
    return dict(notif="Notif")

@auth.requires_signature()
def admin_data_univ():
    rows = db(db.university.approved==False).select(db.university.ALL, orderby=~db.university.created_on)
    d = [{'id':r.id,'name': r.name,'lat': r.lat,'lng':r.lng,'country':r.country,'info':r.info,'class':'danger'}
         for r in rows]
    rows = db(db.university.approved==True).select(db.university.ALL, orderby=~db.university.created_on)
    e = [{'id':r.id,'name': r.name,'lat': r.lat,'lng':r.lng,'country':r.country,'info':r.info,'class':'','approved':r.approved}
         for r in rows]
    f = [i+1 for i in range(0,((len(e)+len(d))/5)+1)]
    return response.json(dict(result=d,result_v=e,pages=f))

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
    query = db.grad.approved==False
    query &= db.grad.refused==False
    rows = db(query).select(db.grad.ALL, orderby=~db.grad.modified_on)
    d = [{'id':r.id,'student': r.student.first_name+' '+r.student.last_name,'university': r.university.name,'link_blog':r.blog,
          'file_link':r.picture.file_link,'quote':r.yr_quote}
         for r in rows]
    f = [i+1 for i in range(0,(len(d)/3)+1)]
    return response.json(dict(result=d,pages=f))


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


@auth.requires_signature()
def profile_edit_simple():
    db.auth_user.update_or_insert((db.auth_user.id == auth.user_id),major=request.vars.major)
    return 'ok'


def create_users():
    raw_users = csv_to_dict()
    for entry in raw_users:
        user = db.auth_user.insert(first_name=entry['first_name'], last_name=entry['last_name'],email=entry['email'],promotion=entry['promotion'],password='')
        auth.email_reset_password(db(db.auth_user.id == user).select().first())

    #for user in db(db.auth_user.password == '').select():
    #    auth.email_reset_password(user)
    return 'ok'


def check_univ_value(univ):
    if univ is not None:
        return univ.name
    return ""

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
    user_prom = None
    if auth.is_logged_in():
        user_prom = db(db.auth_user.id == auth.user_id).select(db.auth_user.promotion).first().promotion
    user_data = {
        'id':'',
        'university':'',
        'link_blog':'',
        'file_link':'',
        'quote':'',
        'refused':False,
        'refused_message':''
    }
    if request.args(0)=='profile' and user_prom <= YEAR-2:
        #First check if user is in grad db
        is_in = db(db.grad.student == auth.user_id).select(db.grad.id).first()
        if is_in is None:
            refused=True
            message = "You can now add new information to your profile. Don't forget that if a profile is complete, it will be used on a public page."
            db.grad.insert(student=auth.user_id,refused=refused,refused_message=message)
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
        d = [{'id':r.id,'university': check_univ_value(r.university),'link_blog':r.blog,
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
    elif request.args(0)=='profile' and user_prom > YEAR-2:
        tmp_data = db(db.auth_user.id==auth.user_id).select(db.auth_user.ALL).first()
        user_data = {
            'major':tmp_data.major,
            'name':tmp_data.first_name+' '+tmp_data.last_name,
            'promo':tmp_data.promotion,
            'email':tmp_data.email
        }
    return dict(form=auth(),grad_data=user_data,user_prom=user_prom)


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


def set_timezone():
    """Ajax call to set the timezone information for the session."""
    tz_name = request.vars.name
    from pytz import all_timezones_set
    if tz_name in all_timezones_set:
        session.user_timezone = tz_name
