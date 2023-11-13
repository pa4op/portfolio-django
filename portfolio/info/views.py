from django.shortcuts import render
from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_week():
    current_week = datetime.now().isocalendar()[1]
    start_week = datetime.now().replace(month=9, day=1).isocalendar()[1]
    week = current_week - start_week + 1
    return week



def index(request):
    context = {}
    return render(request, 'info/index.html', context)



def get_table(group, week):
    req = requests.get(f'https://eners.kgeu.ru/apish2.php?group={group}&week={week}&type=one')
    src = req.text
    soup = BeautifulSoup(src, 'html.parser')
    days = soup.findAll('div', class_='card')

    days_list = []
    for day in days:
        day_info = {'day_name': day.a.string.strip(), 'subjects': []}
        items = day.select('.list-group-item')
        for item in items:
            time = '-'.join(item.select_one('.col-sm-2').text.strip().split(' '))
            subject = item.select_one('.col-sm-6').text.strip()
            cabinet = item.select_one('.col-sm-4 .tx-normal').text.strip()
            instructor = item.select_one('.col-sm-4 .text-muted').text.strip()

            item_info = {
                # 'index': k + 1,
                'time': time,
                'subject': subject,
                'cabinet': cabinet,
                'instructor': instructor
            }
            day_info['subjects'].append(item_info)
        days_list.append(day_info)

    return days_list

def schedule(request):
    week = get_week()
    group = 'ПИ-1-21'
    addgroup = 'ЦК-ДО-5'
    schedule = get_table(group, week)
    add_schedule = get_table(addgroup, week)
    for day in schedule:
        for add_day in add_schedule:
            if add_day['day_name'] == day['day_name']:
                day['subjects'].extend(add_day['subjects'])

    context = {'schedule': schedule}

    return render(request, 'info/schedule.html', context)
    # print(context)
    # another_group_context = get_table(addgroup, week)
    # for day, day_info in another_group_context.items():
    #     day_items = context['schedule'].setdefault(day, {'subjects': {}})
    #     last_index = max(day_items['subjects'].keys(), default=0)
    #     for index, item_info in day_info['subjects'].items():
    #         day_items['subjects'][last_index + index] = item_info

    # print(context['days'])
    # print(len(context['days']))
