types = ['Documents','Classes','Campus Life','Other','']
types_icon = [I(_class="fa fa-file"),I(_class="fa fa-graduation-cap"),I(_class="fa fa-beer"),I(_class="fa fa-question-circle"),I(_class="fa fa-ban")]
idC = 0


def SELECT_TYPE():
    id = "select"+str(idC)
    return SELECT(types, _class='selectpicker', _id=id, _title=T('Subject...'), data={'width':'100px'})


def get_icon(text):
    i = types.index(text)
    return types_icon[i]