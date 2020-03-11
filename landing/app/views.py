from collections import Counter
from django.shortcuts import render_to_response

counter_show = Counter()
counter_click = Counter()


def test_ab_get_param(param):
    """

    (string) -> bool or None

    Function detect value of string param

    """

    if param == 'original':
        return True
    elif param == 'test':
        return False


def index(request):
    from_landing = request.GET.get('from-landing')
    test = test_ab_get_param(from_landing)

    if test is not None:
        counter_click[from_landing] += 1

    return render_to_response('index.html')


def landing(request):
    ab_test_arg = request.GET.get('ab-test-arg')
    test = test_ab_get_param(ab_test_arg)

    if test is not None:
        if test:
            file_page = 'landing.html'
        else:
            file_page = 'landing_alternate.html'
        counter_show[ab_test_arg] += 1
    else:
        file_page = 'index.html'

    return render_to_response(file_page)


def get_conversion(ab_name):
    """

    (string) -> int

    Function gets conversion clicks by shows

    """

    cnt_show = counter_show.get(ab_name, 0)
    cnt_click = counter_click.get(ab_name, 0)
    if cnt_show != 0:
        conversion = cnt_click / cnt_show
    else:
        conversion = 0
    return conversion


def stats(request):
    original_conversion = get_conversion('original')
    test_conversion = get_conversion('test')

    return render_to_response('stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
