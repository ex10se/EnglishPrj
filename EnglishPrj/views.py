import json
import os
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from .forms import *


# получение копии json
def get_json(name):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_json = os.path.join(base_dir, name)
    with open(os.path.join(path_json), encoding="utf-8") as json_data:
        d = json.load(json_data)
    return d


# проверяет, пытается ли посетитель войти в сервис, просто вбив в url строку адрес
# True / False
def check_user():
    f = open("temp_current_user_id.txt", 'r')
    str_id = f.readline()
    f.close()
    if not str_id or str_id == '':
        return True
    else:
        return False


# обновить json файл
# name - название файла
# new_json - загружаемый файл
def reload_json(name, new_json):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_json = os.path.join(base_dir, name)
    with open(os.path.join(path_json), 'w', encoding="utf-8") as jf:
        json.dump(new_json, jf, indent=1)


# авторизация
def login(request):
    if request.method == 'POST':
        form = IdForm(request.POST)
        if form.is_valid():
            users = get_json('users.json')
            for i in users:
                if i['login'] == form.cleaned_data['login'] and i['password'] == form.cleaned_data['password']:
                    str_id = i['id']
                    f = open('temp_current_user_id.txt', "w")
                    f.write(str(str_id))
                    f.close()
                    break
            else:
                return render(request, 'login.html', {'form': form})

            f = open("temp_current_user_id.txt", 'r')
            str_id = f.readline()
            f.close()

            d = get_json("users.json")
            access = 'student'
            for i in d:
                if str(i['id']) == str_id:
                    access = i['access']
                    break

            # я спер кусок кода он внизу(тот который отвечает за список групп)
            # ссылка тоже неверная
            return HttpResponseRedirect('http://127.0.0.1:8000/main')
            # schedule
    else:
        form = IdForm()

    return render(request, 'login.html', {'form': form})


def main(request):
    return render(request, 'main.html')


def schedule(request):
    return render(request, 'schedule.html')


def att(request):
    return render(request, 'att.html')


def cons(request):
    return render(request, 'cons.html')


def notif(request):
    return render(request, 'notif.html')


def faq(request):
    return render(request, 'faq.html')


# деавторизация
def logout(request):
    f = open('temp_current_user_id.txt', 'w')
    f.close()
    return HttpResponseRedirect('http://127.0.0.1:8000')


# личный профиль
def profile(request):
    #  проверка, произведен ли вход
    test_user = check_user()
    if test_user:
        return HttpResponseRedirect("http://127.0.0.1:8000")

    f = open("temp_current_user_id.txt", 'r')
    current_id = f.readline()
    f.close()
    d = get_json('users.json')
    g = get_json('groups.json')
    for i in d:
        if str(i['id']) == str(current_id):
            access_str = i['access']
            lastname_str = i['lastname']
            name_str = i['name']
            middlename_str = i['middlename']
            if access_str == 'teacher':
                groups_str = []
                for j in g:
                    if j['teacher-id'] == i['id']:
                        groups_str.append(j)
            else:
                for j in g:
                    for k in j['student-ids'].split(','):
                        if str(i['id']) == k:
                            group_str = j
            break
    return render(request, 'profile.html', locals())


# распиание(главная страница)
# def schedule(request):
#     #  проверка, произведен ли вход
#     test_user = check_user()
#     if test_user:
#         return HttpResponseRedirect("http://127.0.0.1:8000")

# def group_list(request):


# в менюшке по переходу в профиль
# d = get_json("groups.json")
#           array = []
#
#           for i in range(len(d)):
#               if d[i]['teacher-id'] or d[i]['student-ids'] == int(str_id):
#                  array.append(d[i])
