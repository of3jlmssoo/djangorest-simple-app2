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
    'confirmed': 0, # confirm画面を制御。最初(==0)は確認を行い、選択肢は確定と戻る。確定した場合(==1)選択肢は戻るのみとなる
    'thousands': 0,
    'millions': 0,
    'price': 0,
    'box': 0,
    'proc': 0,
    'message': '',
    'message2': '',
    'chokinkakutei': DISABLED_BUTTON,
}
"""
confirmedの推移
1. 貯金箱、処理、金額が指定される               confirmed == 0
2. confirm.htmlが呼ばれる。                     confirmed == 0
    confirmed == 1なので確定ボタンと戻るボタンが利用可能
        確定ボタン 再びconfirm.htmlへ。この際thousands=0 millions=0がパラメータとして使われる
        戻るボタン chokin.htmlへ
        (thousands=0 millions=0は1.の画面からコールされた場合は無い組み合わせ)
3. views.py def confirm()でthousands=0 millions=0の場合
        choice_context['confirmed'] = 1         confirmed == 1
        set_current() (box?currentを更新し、かつ、DBに新しい額を設定する)
    が実行される。
    その後return renderでchokin.htmlへ
4. views.py def chokin()ではconfirmed == 1の場合
    貯金箱選択と処理選択をクリアし
    金額指定をクリアし
    confirmedを0にする                          confirmed == 0
"""



def proc_bill(request, target, proc):
    """ 金額指定のboxprice1.html/boxprice2.htmlの中で、+ボタン、-ボタンがクリックされるとコールされる
    """
    # + or -のクリック後の金額が想定の範囲内であれば+1 or -1する
    if target == 'thousands' and proc == '+' and choice_context['thousands'] < 9:
        choice_context['thousands'] += 1
    if target == 'millions' and proc == '+' and choice_context['millions'] < 20:
        choice_context['millions'] += 1

    if target == 'thousands' and proc == '-' and choice_context['thousands'] > 0:
        choice_context['thousands'] -= 1
    if target == 'millions' and proc == '-' and choice_context['millions'] > 0:
        choice_context['millions'] -= 1

    # 貯金箱が選択され、処理が選択されていれば確定ボタンを使えるようにするが
    # 金額指定が行われていない場合disable状態にする
    if HIGHLIGHT_CLASS in [
            choice_context['box1'],
            choice_context['box2'],
            choice_context['box3']] and HIGHLIGHT_CLASS in [
            choice_context['proc1'],
            choice_context['proc2']]:
        choice_context['chokinkakutei'] = NORMAL_BUTTON

    if choice_context['millions'] == 0 and choice_context['thousands'] == 0:
        choice_context['chokinkakutei'] = DISABLED_BUTTON

    # 金額を'price'に保持する
    choice_context['price'] = choice_context['millions'] * 10 + choice_context['thousands']
    return redirect('chokin')


def select_box(request, id):
    """ boxes.htmlで貯金箱が選ばれるとコールされる
    """
    # 一旦全ての貯金箱をNORMALに設定し、その後貯金箱選択肢のチェックを行う
    # その後選ばれた貯金箱をHIGHLIGHTにする
    choice_context['box1'] = NORMAL_CLASS
    choice_context['box2'] = NORMAL_CLASS
    choice_context['box3'] = NORMAL_CLASS

    # 貯金箱数は3を前提
    if id < 1 or id > 3:
        print(f'chokin views.py select_box: invalid box choice {id=}')

    if id == 1: choice_context['box1'] = HIGHLIGHT_CLASS
    if id == 2: choice_context['box2'] = HIGHLIGHT_CLASS
    if id == 3: choice_context['box3'] = HIGHLIGHT_CLASS

    # 他の選択肢が選ばれていれば確定ボンタンをイネーブルする
    # 他の選択肢 処理(proc)と価格指定
    if (HIGHLIGHT_CLASS in [choice_context['proc1'], choice_context['proc2']]) and (choice_context['millions'] > 0 or choice_context['thousands'] > 0):
        choice_context['chokinkakutei'] = NORMAL_BUTTON

    return redirect('chokin')


def select_proc(request, id):
    """ boxprocprice.htmlで処理が選ばれるとコールされる
    """
    # 一旦両方の処理(貯める、使う）をNORMALに設定し、その後選択肢のチェックを行う
    # その後選ばれた処理をHIGHLIGHTにする

    choice_context['proc1'] = NORMAL_CLASS
    choice_context['proc2'] = NORMAL_CLASS

    if id < 1 or id > 2:
        print(f'chokin views.py select_box: invalid box choice {id=}')

    if id == 1: choice_context['proc1'] = HIGHLIGHT_CLASS
    if id == 2: choice_context['proc2'] = HIGHLIGHT_CLASS

    # 他の選択肢が選ばれていれば確定ボンタンをイネーブルする
    # 他の選択肢 貯金箱と価格指定
    if (HIGHLIGHT_CLASS in [choice_context['box1'], choice_context['box2'], choice_context['box3']]) and (
            choice_context['millions'] > 0 or choice_context['thousands'] > 0):
        choice_context['chokinkakutei'] = NORMAL_BUTTON

    return redirect('chokin')


def chokin(request):
    """ 実質的な初期画面
    """

    # モデルアクセス準備
    if box_objects['box1'] is None:
        box_objects['box1'] = Chokinbako.objects.get(chokinbako_name='box1')
        box_objects['box2'] = Chokinbako.objects.get(chokinbako_name='box2')
        box_objects['box3'] = Chokinbako.objects.get(chokinbako_name='box3')
        choice_context['box1current'] = box_objects['box1'].chokinbako_value
        choice_context['box2current'] = box_objects['box2'].chokinbako_value
        choice_context['box3current'] = box_objects['box3'].chokinbako_value

    if choice_context['confirmed'] == 1:
        # 上記、confirmedの推移、参照        
        clear_choices() # 貯金箱選択と処理選択をクリアする
        choice_context['confirmed'] = 0 # ステータスをクリアする

    # 画面表示を３桁区切りにする
    choice_context['box1display'] = "{:,}".format(choice_context['box1current'])
    choice_context['box2display'] = "{:,}".format(choice_context['box2current'])
    choice_context['box3display'] = "{:,}".format(choice_context['box3current'])

    return render(request, 'chokin/chokin.html', choice_context)


def clear_choices():
    choice_context['box1'] = NORMAL_CLASS
    choice_context['box2'] = NORMAL_CLASS
    choice_context['box3'] = NORMAL_CLASS
    choice_context['proc1'] = NORMAL_CLASS
    choice_context['proc2'] = NORMAL_CLASS
    choice_context['millions'] = 0  # 金額指定をクリアする
    choice_context['thousands'] = 0 # 金額指定をクリアする
    choice_context['price'] = 0 # 金額指定をクリアする


def which_box_and_process():
    """ 選択された貯金箱と処理を返す
    """
    return [k for k, v in choice_context.items() if v == HIGHLIGHT_CLASS]



def resetchokin(request):
    """ 処金箱選択、処理選択、金額指定をクリアする。chokin.htmlの下右のリセットボタンに対応
    """
    clear_choices()
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

def set_curretn_details(boxcurrent, box, proc):
    if proc == "+":
        choice_context[boxcurrent] += choice_context['price'] * 1000
    else:
        choice_context[boxcurrent] -= choice_context['price'] * 1000
    box_objects[box].chokinbako_value = choice_context[boxcurrent]
    box_objects[box].save()


def set_current():
    if choice_context['proc'] == 'proc1':
        if choice_context['box'] == 'box1':
            set_curretn_details('box1current', 'box1', "+")
        elif choice_context['box'] == 'box2':
            set_curretn_details('box2current', 'box2', "+")
        elif choice_context['box'] == 'box3':
            set_curretn_details('box3current', 'box3', "+")
    elif choice_context['proc'] == 'proc2':
        if choice_context['box'] == 'box1':
            set_curretn_details('box1current', 'box1', "-")
        elif choice_context['box'] == 'box2':
            set_curretn_details('box2current', 'box2', "-")
        elif choice_context['box'] == 'box3':
            set_curretn_details('box3current', 'box3', "-")


def access_to_db():

    q = Chokinbako.objects.get(chokinbako_name='box1')
    print(f'{q.chokinbako_value=}')
    q.chokinbako_value = 200000
    q.save()


def confirm(request, thousands, millions):
    print(f"============> {choice_context['confirmed']=} {thousands=} {millions=}")

    # access_to_db()

    # 最初のconfirm.htmlから呼ばれるとthousands == 0 and millions == 0
    if thousands == 0 and millions == 0:
        choice_context['confirmed'] = 1
        # confirm.htmlの"今回"を算出する。選ばれた貯金箱以外は0になる
        # 選ばれた貯金箱の"今回"は貯めるの場合"+"が付けられ、"使う"の場合"-"が付けられる
        # set_current()で対象処金箱が特定され、かつ、符号が処理される
        #   set_current_details()で
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
        # choice_context['subpanel'] = 1

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
