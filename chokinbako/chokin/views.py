from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


HIGHLIGHT_CLASS = "btn btn-success w-100 btn-lg rounded-pill"
NORMAL_CLASS = "btn btn-secondary w-100 btn-lg rounded-pill"

choice_context = {
    'attr1': NORMAL_CLASS,
    'attr2': NORMAL_CLASS,
    'attr3': NORMAL_CLASS,
    'attr4': NORMAL_CLASS,
    'attr5': NORMAL_CLASS,
    'attr6': NORMAL_CLASS,
}


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'chokin/base.html', choice_context)


def some_view(request):
    print(f'=> some_view() called {request.POST.keys()}')
    context = {
        'attr1': NORMAL_CLASS,
        'attr2': NORMAL_CLASS,
        'attr3': NORMAL_CLASS,
    }

    if 'boxchoice1' in request.POST:
        choice_context['attr1'] = HIGHLIGHT_CLASS
        choice_context['attr2'] = NORMAL_CLASS
        choice_context['attr3'] = NORMAL_CLASS
    if 'boxchoice2' in request.POST:
        choice_context['attr1'] = NORMAL_CLASS
        choice_context['attr2'] = HIGHLIGHT_CLASS
        choice_context['attr3'] = NORMAL_CLASS
    if 'boxchoice3' in request.POST:
        choice_context['attr1'] = NORMAL_CLASS
        choice_context['attr2'] = NORMAL_CLASS
        choice_context['attr3'] = HIGHLIGHT_CLASS

    if 'boxchoice4' in request.POST:
        choice_context['attr4'] = HIGHLIGHT_CLASS
        choice_context['attr5'] = NORMAL_CLASS
    if 'boxchoice5' in request.POST:
        choice_context['attr4'] = NORMAL_CLASS
        choice_context['attr5'] = HIGHLIGHT_CLASS

    print(f'{choice_context=}')

    return render(request, 'chokin/base.html', choice_context)
