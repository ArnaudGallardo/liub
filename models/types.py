types_icon = [I(_class="fa fa-file"),I(_class="fa fa-graduation-cap"),I(_class="fa fa-beer"),I(_class="fa fa-question-circle")]
idC = 0


def SELECT_TYPE():
    id = "select"+str(idC)
    return SELECT(TYPES, _class='selectpicker', _id=id, _title=T('Subject...'), data={'width':'100px'})


def get_icon(text):
    i = TYPES.index(text)
    return types_icon[i]

def get_lg_major(text):
    i = MAJOR.index(text)
    return MAJOR_LG[i]

def get_major_obj(selected):
    opt = []
    for i in range(0,len(MAJOR)):
        if MAJOR[i]==selected:
            opt.append(OPTION(MAJOR_LG[i],_value=MAJOR[i],_selected="selected"))
        else:
            opt.append(OPTION(MAJOR_LG[i],_value=MAJOR[i]))
    return opt