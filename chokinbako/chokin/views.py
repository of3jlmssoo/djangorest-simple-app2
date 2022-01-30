from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.template import loader

HIGHLIGHT_CLASS = "btn btn-success w-100 btn-lg rounded-pill p-4"
NORMAL_CLASS = "btn btn-secondary w-100 btn-lg rounded-pill p-4"

choice_context = {
    'box1': NORMAL_CLASS,
    'box2': NORMAL_CLASS,
    'box3': NORMAL_CLASS,
    'proc1': NORMAL_CLASS,
    'proc2': NORMAL_CLASS,
    'box1current': 321,
    'box2current': 654,
    'box3current': 987,
    'box1previous': 123,
    'box2previous': 456,
    'box3previous': 789,
    'boxpanel': 0,
    'subpanel': 0,
    'price': 0,
    'box': 0,
    'proc': 0
}


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'chokin/base.html', choice_context)


def chokin(request):
    print(f'=> chokin()() called {request.POST.keys()}')
    # context = {
    #     'box1': NORMAL_CLASS,
    #     'box2': NORMAL_CLASS,
    #     'box3': NORMAL_CLASS,
    # }

    if 'boxchoice1' in request.POST:
        choice_context['box1'] = HIGHLIGHT_CLASS
        choice_context['box2'] = NORMAL_CLASS
        choice_context['box3'] = NORMAL_CLASS
    if 'boxchoice2' in request.POST:
        choice_context['box1'] = NORMAL_CLASS
        choice_context['box2'] = HIGHLIGHT_CLASS
        choice_context['box3'] = NORMAL_CLASS
    if 'boxchoice3' in request.POST:
        choice_context['box1'] = NORMAL_CLASS
        choice_context['box2'] = NORMAL_CLASS
        choice_context['box3'] = HIGHLIGHT_CLASS
    if 'boxchoice4' in request.POST:
        choice_context['proc1'] = HIGHLIGHT_CLASS
        choice_context['proc2'] = NORMAL_CLASS
    if 'boxchoice5' in request.POST:
        choice_context['proc1'] = NORMAL_CLASS
        choice_context['proc2'] = HIGHLIGHT_CLASS
    if 'price1' in request.POST:
        print(f'=> chokin()() called {request.POST.get("price1")=} {which_box_and_process()=}')
        # return redirect('result')
        # return render(request, 'chokin/result.html', request.POST.get("price1"),which_box_and_process())

        # price = request.POST.get("price1")
        choice_context['price'] = request.POST.get("price1")
        box_proc = which_box_and_process()
        choice_context['box'] = box_proc[0]
        choice_context['proc'] = box_proc[1]
        print(f'=========================> {box_proc=}')

        # template=loader.get_template('chokin/result.html')
        # context ={'price':price,'box':box_proc[0], 'proc':box_proc[1]}
        # return HttpResponse(template.render(context,request))

        # return HttpResponse("Hello, World!")
        return redirect('confirm')
        # return render(request, 'chokin/result.html', {'price':price,'box':box_proc[0], 'proc':box_proc[1]})

        # result(request, price,box_proc[0], box_proc[1])

    # return render(request, 'chokin/base.html', choice_context)
    return render(request, 'chokin/chokin.html', choice_context)


def clear_choices():
    choice_context['box1'] = NORMAL_CLASS
    choice_context['box2'] = NORMAL_CLASS
    choice_context['box3'] = NORMAL_CLASS
    choice_context['proc1'] = NORMAL_CLASS
    choice_context['proc2'] = NORMAL_CLASS


def which_box_and_process():
    print(f'which_box_and_process() called {choice_context=}')
    # TODO: 有効な組み合わせであるかチェックする。駄目ならやり直しを求める
    return [k for k, v in choice_context.items() if v == HIGHLIGHT_CLASS]
    pass


def which_process():
    pass


def confirm(request):
    # return redirect('result')

    # template = loader.get_template('chokin/confirm.html')
    # return HttpResponse(template.render(choice_context, request))

    # return HttpResponse("Hello, World!")

    return render(request, 'chokin/confirm.html', choice_context)
