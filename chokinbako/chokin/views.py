from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


HIGHLIGHT_CLASS = "btn btn-success w-100 btn-lg rounded-pill p-4"
NORMAL_CLASS = "btn btn-secondary w-100 btn-lg rounded-pill p-4"

choice_context = {
    'box1': NORMAL_CLASS,
    'box2': NORMAL_CLASS,
    'box3': NORMAL_CLASS,
    'proc1': NORMAL_CLASS,
    'proc2': NORMAL_CLASS,
    'attr6': NORMAL_CLASS,
}


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'chokin/base.html', choice_context)


def some_view(request):
    print(f'=> some_view() called {request.POST.keys()}')
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
        print(f'=> some_view() called {request.POST.get("price1")=} {which_box_and_process()=}')
        choice_context['box1'] = NORMAL_CLASS
        choice_context['box2'] = NORMAL_CLASS
        choice_context['box3'] = NORMAL_CLASS
        choice_context['proc1'] = NORMAL_CLASS
        choice_context['proc2'] = NORMAL_CLASS
    
    print(f'{choice_context=}')
    return render(request, 'chokin/base.html', choice_context)

def which_box_and_process():
    print(f'which_box_and_process() called {choice_context=}')
    return [k for k, v in choice_context.items() if v == HIGHLIGHT_CLASS]
    pass
def which_process():
    pass
