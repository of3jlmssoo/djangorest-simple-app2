from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages

HIGHLIGHT_CLASS = "btn btn-success   w-100 btn-lg rounded-pill p-4"
NORMAL_CLASS = "btn btn-secondary w-100 btn-lg rounded-pill p-4"

choice_context = {
    'box1': NORMAL_CLASS,
    'box2': NORMAL_CLASS,
    'box3': NORMAL_CLASS,
    'proc1': NORMAL_CLASS,
    'proc2': NORMAL_CLASS,
    'box1display': 200000,  # formatted string with thousand separator
    'box2display': 100000,  # formatted string with thousand separator
    'box3display': 50000,   # formatted string with thousand separator
    'box1current': 200000,  # int
    'box2current': 100000,  # int
    'box3current': 50000,   # int
    'box1previous': 123,    # int
    'box2previous': 456,    # int
    'box3previous': 789,    # int
    'boxpanel': 0,
    'subpanel': 0,
    'thousands': 0,
    'millions': 0,
    'price': 0,
    'box': 0,
    'proc': 0,
    'message': '',
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

    return redirect('chokin')


def select_proc(request, id):
    # print(f'chokin views.py select_proc: called')
    choice_context['proc1'] = NORMAL_CLASS
    choice_context['proc2'] = NORMAL_CLASS

    if id < 1 or id > 2:
        print(f'chokin views.py select_box: invalid box choice {id=}')

    if id == 1: choice_context['proc1'] = HIGHLIGHT_CLASS
    if id == 2: choice_context['proc2'] = HIGHLIGHT_CLASS

    return redirect('chokin')


def chokin(request):
    # print(f'=> chokin() called {request.POST.keys()}')

    choice_context['box1display'] = "{:,}".format(choice_context['box1current'])
    choice_context['box2display'] = "{:,}".format(choice_context['box2current'])
    choice_context['box3display'] = "{:,}".format(choice_context['box3current'])
    choice_context['subpanel'] = 0
    # context = {
    #     'box1': NORMAL_CLASS,
    #     'box2': NORMAL_CLASS,
    #     'box3': NORMAL_CLASS,
    # }

    # if 'boxchoice1' in request.POST:
    #     choice_context['box1'] = HIGHLIGHT_CLASS
    #     choice_context['box2'] = NORMAL_CLASS
    #     choice_context['box3'] = NORMAL_CLASS
    # if 'boxchoice2' in request.POST:
    #     choice_context['box1'] = NORMAL_CLASS
    #     choice_context['box2'] = HIGHLIGHT_CLASS
    #     choice_context['box3'] = NORMAL_CLASS
    # if 'boxchoice3' in request.POST:
    #     choice_context['box1'] = NORMAL_CLASS
    #     choice_context['box2'] = NORMAL_CLASS
    #     choice_context['box3'] = HIGHLIGHT_CLASS
    # if 'boxchoice4' in request.POST:
    #     choice_context['proc1'] = HIGHLIGHT_CLASS
    #     choice_context['proc2'] = NORMAL_CLASS
    # if 'boxchoice5' in request.POST:
    #     choice_context['proc1'] = NORMAL_CLASS
    #     choice_context['proc2'] = HIGHLIGHT_CLASS
    # if 'price1' in request.POST:
    #     # print(f'=> chokin()() called {request.POST.get("price1")=} {which_box_and_process()=}')
    #     # return redirect('result')
    #     # return render(request, 'chokin/result.html', request.POST.get("price1"),which_box_and_process())

    #     # price = request.POST.get("price1")
    #     choice_context['price'] = request.POST.get("price1")
    #     box_proc = which_box_and_process()
    #     choice_context['box'] = box_proc[0]
    #     choice_context['proc'] = box_proc[1]

    #     # template=loader.get_template('chokin/result.html')
    #     # context ={'price':price,'box':box_proc[0], 'proc':box_proc[1]}
    #     # return HttpResponse(template.render(context,request))

    #     # return HttpResponse("Hello, World!")
    #     return redirect('confirm')
    #     # return render(request, 'chokin/result.html', {'price':price,'box':box_proc[0], 'proc':box_proc[1]})

    #     # result(request, price,box_proc[0], box_proc[1])

    # return render(request, 'chokin/base.html', choice_context)
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
    return render(request, 'chokin/chokin.html', choice_context)


def confirm(request, thousands, millions):
    # return redirect('result')

    # template = loader.get_template('chokin/confirm.html')
    # return HttpResponse(template.render(choice_context, request))

    # return HttpResponse("Hello, World!")
    result = which_box_and_process()
    print(f'confirm() {result=} {len(result)=}')
    if len(result) != 2:
        messages.error(request, '貯金箱と処理の選択が無効です。2つ共選んでください')

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

    # 1000円を　貯金箱1   から引き出します。
    # 1000円を　貯金箱1  で貯めます。
    print(f"{choice_context['box']=} {choice_context['proc']=}")
    if choice_context['box'] == 'box1':
        box = '貯金箱1'
    elif choice_context['box'] == 'box2':
        box = '貯金箱2'
    elif choice_context['box'] == 'box3':
        box = '貯金箱3'
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
    return render(request, 'chokin/confirm.html', choice_context)
