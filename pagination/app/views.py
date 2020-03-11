from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
import csv
from urllib.parse import urlencode


def get_url_by_page_number(page_number):
    """

    (int) -> string

    Function gets url by page number

    """

    url_root = f"{reverse(bus_stations)}?"
    url_params = urlencode({'page': page_number})
    return url_root + url_params


def index(request):
    url = get_url_by_page_number(1)
    return redirect(url)


def bus_stations(request):
    page_number = request.GET.get('page', 1)
    print(f"page_number = {page_number}")

    # Read from csv file
    with open(settings.BUS_STATION_CSV, encoding='cp1251') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        csv_list = list(reader)
        p = Paginator(csv_list[1::1], 10)
        page = p.get_page(page_number)

        if page.has_next():
            next_page_url = get_url_by_page_number(page.next_page_number())
        else:
            next_page_url = None

        if page.has_previous():
            prev_page_url = get_url_by_page_number(page.previous_page_number())
        else:
            prev_page_url = None

        bus_stations_list = list()
        for row in page.object_list:
            row_dict = {'Name': row['Name'], 'Street': row['Street'], 'District': row['District']}
            bus_stations_list.append(row_dict)

    return render_to_response('index.html', context={
        'bus_stations': bus_stations_list,
        'current_page': page_number,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })
