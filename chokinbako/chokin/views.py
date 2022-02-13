from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import Chokinbako

HIGHLIGHT_CLASS = "btn btn-success   w-100 btn-lg rounded-pill p-4"
NORMAL_CLASS = "btn btn-secondary w-100 btn-lg rounded-pill p-4"

NORMAL_BUTTON = "btn btn-primary btn-sm"
DISABLED_BUTTON = "btn btn-primary btn-sm disabled"

MAX_DEPOSIT = 300000
MIN_DEPOSIT = 0

box_objects = {
    'box1': None,
    'box2': None,
    'box3': None,
}
choice_context = {
    'box1': NORMAL_CLASS,
    'box2': NORMAL_CLASS,
    'box3': NORMAL_CLASS,
    'proc1': NORMAL_CLASS,
    'proc2': NORMAL_CLASS,
    'box1display': None,  # formatted string with thousand separator
    'box2display': None,  # formatted string with thousand separator
    'box3display': None,   # formatted string with thousand separator
    'box1current': None,  # int
    'box2current': None,  # int
    'box3current': None,   # int
    'box1previous': None,    # int
    'box2previous': None,    # int
    'box3previous': None,    # int
    'box1thistime': 0,
    'box2thistime': 0,
    'box3thistime': 0,
    'box1after': 0,
    'box2after': 0,
    'box3after': 0,
    'box1afterattribute': "",
    'box2afterattribute': "",
    'box3afterattribute': "",
    'confirmed': 0,
    'boxpanel': 0,
    'subpanel': 0,
    'thousands': 0,
    'millions': 0,
    'price': 0,
    'box': 0,
    'proc': 0,
    'message': '',
    'message2': '',
    'chokinkakutei': DISABLED_BUTTON,
}


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'chokin/base.html', choice_context)


def proc_bill(request, target, proc):
    if target == 'thousands' and proc == '+' and choice_context['thousands'] < 9:
        choice_context['thousands'] += 1
    if target == 'millions' and proc == '+' and choice_context['millions'] < 20:
        choice_context['millions'] += 1

    if target == 'thousands' and proc == '-' and choice_context['thousands'] > 0:
        choice_context['thousands'] -= 1
    if target == 'millions' and proc == '-' and choice_context['millions'] > 0:
        choice_context['millions'] -= 1

    if HIGHLIGHT_CLASS in [
            choice_context['box1'],
            choice_context['box2'],
            choice_context['box3']] and HIGHLIGHT_CLASS in [
            choice_context['proc1'],
            choice_context['proc2']]:
        choice_context['chokinkakutei'] = NORMAL_BUTTON

    if choice_context['millions'] == 0 and choice_context['thousands'] == 0:
        choice_context['chokinkakutei'] = DISABLED_BUTTON

    choice_context['price'] = choice_context['millions'] * 10 + choice_context['thousands']
    return redirect('chokin')


def select_box(request, id):
    # print(f'chokin views.py select_box: called')
    choice_context['box1'] = NORMAL_CLASS
    choice_context['box2'] = NORMAL_CLASS
    choice_context['box3'] = NORMAL_CLASS

    if id < 1 or id > 3:
        print(f'chokin views.py select_box: invalid box choice {id=}')

    if id == 1: choice_context['box1'] = HIGHLIGHT_CLASS
    if id == 2: choice_context['box2'] = HIGHLIGHT_CLASS
    if id == 3: choice_context['box3'] = HIGHLIGHT_CLASS

    if (HIGHLIGHT_CLASS in [choice_context['proc1'], choice_context['proc2']]) and (choice_context['millions'] > 0 or choice_context['thousands'] > 0):
        choice_context['chokinkakutei'] = NORMAL_BUTTON

    return redirect('chokin')


def select_proc(request, id):
    # print(f'chokin views.py select_proc: called')
    choice_context['proc1'] = NORMAL_CLASS
    choice_context['proc2'] = NORMAL_CLASS

    if id < 1 or id > 2:
        print(f'chokin views.py select_box: invalid box choice {id=}')

    if id == 1: choice_context['proc1'] = HIGHLIGHT_CLASS
    if id == 2: choice_context['proc2'] = HIGHLIGHT_CLASS

    if (HIGHLIGHT_CLASS in [choice_context['box1'], choice_context['box2'], choice_context['box3']]) and (
            choice_context['millions'] > 0 or choice_context['thousands'] > 0):
        choice_context['chokinkakutei'] = NORMAL_BUTTON

    return redirect('chokin')


def chokin(request):
    # print(f'=> chokin() called {request.POST.keys()}')

    if box_objects['box1'] is None:
        box_objects['box1'] = Chokinbako.objects.get(chokinbako_name='box1')
        box_objects['box2'] = Chokinbako.objects.get(chokinbako_name='box2')
        box_objects['box3'] = Chokinbako.objects.get(chokinbako_name='box3')
        choice_context['box1current'] = box_objects['box1'].chokinbako_value
        choice_context['box2current'] = box_objects['box2'].chokinbako_value
        choice_context['box3current'] = box_objects['box3'].chokinbako_value

    if choice_context['confirmed'] == 1:
        clear_choices()
        choice_context['confirmed'] = 0
        choice_context['millions'] = 0
        choice_context['thousands'] = 0
        choice_context['price'] = 0

    choice_context['box1display'] = "{:,}".format(choice_context['box1current'])
    choice_context['box2display'] = "{:,}".format(choice_context['box2current'])
    choice_context['box3display'] = "{:,}".format(choice_context['box3current'])
    choice_context['subpanel'] = 0
    return render(request, 'chokin/chokin.html', choice_context)


def clear_choices():
    choice_context['box1'] = NORMAL_CLASS
    choice_context['box2'] = NORMAL_CLASS
    choice_context['box3'] = NORMAL_CLASS
    choice_context['proc1'] = NORMAL_CLASS
    choice_context['proc2'] = NORMAL_CLASS


def which_box_and_process():
    # print(f'which_box_and_process() called {choice_context=}')
    # TODO: 有効な組み合わせであるかチェックする。駄目ならやり直しを求める
    return [k for k, v in choice_context.items() if v == HIGHLIGHT_CLASS]
    pass


def which_process():
    pass


def resetchokin(request):

    print(f'--> return2chokin called {request.POST=}')
    clear_choices()
    choice_context['boxpanel'] = 0
    choice_context['subpanel'] = 0
    choice_context['millions'] = 0
    choice_context['thousands'] = 0
    choice_context['price'] = 0

    choice_context['chokinkakutei'] = DISABLED_BUTTON
    return render(request, 'chokin/chokin.html', choice_context)


def set_pricethistime():
    if choice_context['proc'] == 'proc1':
        sign = "+"
    elif choice_context['proc'] == 'proc2':
        sign = "-"
    else:
        sign = ""

    return sign + "{:,}".format(choice_context['price'] * 1000)


def set_afterpriceattribute():
    if choice_context['box'] == 'box1':
        choice_context['box1afterattribute'] = "text-danger"
    elif choice_context['box'] == 'box2':
        choice_context['box2afterattribute'] = "text-danger"
    elif choice_context['box'] == 'box3':
        choice_context['box3afterattribute'] = "text-danger"


def set_currentprice(request):
    currentprice = 0
    if choice_context['box'] == 'box1':
        currentprice = choice_context['box1current']
    elif choice_context['box'] == 'box2':
        currentprice = choice_context['box2current']
    elif choice_context['box'] == 'box3':
        currentprice = choice_context['box3current']
    else:
        messages.error(request, '手続き後の試算でエラーが発生しました(貯金箱の確認でエラー)')

    return currentprice


def check_set_priceafter(request):

    choice_context['box1after'] = 0
    choice_context['box2after'] = 0
    choice_context['box3after'] = 0

    choice_context['box1afterattribute'] = ""
    choice_context['box2afterattribute'] = ""
    choice_context['box3afterattribute'] = ""

    currentprice = 0
    afterprice = 0

    currentprice = set_currentprice(request)

    if choice_context['proc'] == 'proc1':
        afterprice = currentprice + choice_context['price'] * 1000
    elif choice_context['proc'] == 'proc2':
        afterprice = currentprice - choice_context['price'] * 1000
    else:
        messages.error(request, '手続き後の試算でエラーが発生しました(手続きの確認でエラー)')

    if afterprice > MAX_DEPOSIT:
        set_afterpriceattribute()
        messages.error(request, f'貯金額が多すぎます。{"{:,}".format(MAX_DEPOSIT)}までしか貯金できません。')

    if afterprice < MIN_DEPOSIT:
        set_afterpriceattribute()
        messages.error(request, f'使う額が多すぎます。')

    return "{:,}".format(afterprice)


def set_current():
    if choice_context['proc'] == 'proc1':
        if choice_context['box'] == 'box1':
            choice_context['box1current'] += choice_context['price'] * 1000
            box_objects['box1'].chokinbako_value = choice_context['box1current']
            box_objects['box1'].save()
        elif choice_context['box'] == 'box2':
            choice_context['box2current'] += choice_context['price'] * 1000
            box_objects['box2'].chokinbako_value = choice_context['box2current']
            box_objects['box2'].save()
        elif choice_context['box'] == 'box3':
            choice_context['box3current'] += choice_context['price'] * 1000
            box_objects['box3'].chokinbako_value = choice_context['box3current']
            box_objects['box3'].save()
    elif choice_context['proc'] == 'proc2':
        if choice_context['box'] == 'box1':
            choice_context['box1current'] -= choice_context['price'] * 1000
            box_objects['box1'].chokinbako_value = choice_context['box1current']
            box_objects['box1'].save()
        elif choice_context['box'] == 'box2':
            choice_context['box2current'] -= choice_context['price'] * 1000
            box_objects['box2'].chokinbako_value = choice_context['box2current']
            box_objects['box2'].save()
        elif choice_context['box'] == 'box3':
            choice_context['box3current'] -= choice_context['price'] * 1000
            box_objects['box3'].chokinbako_value = choice_context['box3current']
            box_objects['box3'].save()


def access_to_db():

    q = Chokinbako.objects.get(chokinbako_name='box1')
    print(f'{q.chokinbako_value=}')
    q.chokinbako_value = 200000
    q.save()


def confirm(request, thousands, millions):
    print(f"============> {choice_context['confirmed']=} {thousands=} {millions=}")

    # access_to_db()

    if thousands == 0 and millions == 0:
        choice_context['confirmed'] = 1
        set_current()
    else:
        choice_context['confirmed'] = 0

        choice_context['box1thistime'] = 0
        choice_context['box2thistime'] = 0
        choice_context['box3thistime'] = 0
        choice_context['box1after'] = 0
        choice_context['box2after'] = 0
        choice_context['box3after'] = 0

    result = which_box_and_process()
    print(f'confirm() {result=} {len(result)=}')
    if len(result) != 2:
        messages.error(request, '貯金箱と処理の選択が無効です。2つ共選んでください')

    # if len(result) == 2 and choice_context['confirmed'] == 0:
    if len(result) == 2:
        if result[0] not in ['box1', 'box2', 'box3']:
            print(f'confirm error : error at box selection {result=}')
            messages.error(request, '貯金箱を選んでください。')
        if result[1] not in ['proc1', 'proc2']:
            print(f'confirm error : error at process selection  {result=}')
            messages.error(request, '処理を選んでください。')

        choice_context['box'] = result[0]
        choice_context['proc'] = result[1]
        choice_context['subpanel'] = 1

        if choice_context['confirmed'] == 0:
            print(f"{choice_context['box']=} {choice_context['proc']=}")
            if choice_context['box'] == 'box1':
                box = '貯金箱1'
                choice_context['box1after'] = check_set_priceafter(request)
                choice_context['box1thistime'] = set_pricethistime()
            elif choice_context['box'] == 'box2':
                box = '貯金箱2'
                choice_context['box2after'] = check_set_priceafter(request)
                choice_context['box2thistime'] = set_pricethistime()
            elif choice_context['box'] == 'box3':
                box = '貯金箱3'
                choice_context['box3after'] = check_set_priceafter(request)
                choice_context['box3thistime'] = set_pricethistime()
            else:
                print(f'confirm() 貯金箱指定が無効')

            if choice_context['proc'] == 'proc1':
                proc = 'で貯めます。'
            elif choice_context['proc'] == 'proc2':
                proc = 'から引き出します。'
            else:
                print(f'confirm() 処理指定が無効')

            val = millions * 10000 + thousands * 1000
            msg = str(val) + 'を' + box + proc
            choice_context['message'] = msg

            choice_context['message2'] = f"{choice_context['price']=} "

        return render(request, 'chokin/confirm.html', choice_context)
    return render(request, 'chokin/chokin.html', choice_context)
