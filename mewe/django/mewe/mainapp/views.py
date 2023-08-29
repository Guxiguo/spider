from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import os
import json
# Create your views here.
PYTHON38_PATH = 'D:/lib/anaconda/envs/py38/python'
PYTHON37_PATH = 'D:/lib/anaconda/envs/py37/python'
MEWE_SCRIPT_PATH = 'D:/code/spider/mewe/group.py'
LINE_SCRIPT_PATH = 'D:/code/spider/line/line.py'
mewe_save_path = ''
line_save_path = ''


def mewe_web(request):
    return render(request, "mewe.html")


def line_web(request):
    return render(request, "line.html")


def mewe_port(request):
    content = {
        'email': '',
        'password': '',
        'type': '',  # t i
        'type_data': '',
        'interval': '',
        'group': '',
        'save_path': '',
        'browser': '',
        'browser_data': '',
    }
    result = {'returnCode': True,
              }
    if request.method == 'POST':
        content['email'] = request.POST.get('email')
        content['password'] = request.POST.get('password')
        content['type'] = request.POST.get('type')
        content['type_data'] = request.POST.get('type_data')
        content['interval'] = request.POST.get('interval')
        content['group'] = request.POST.get('group')
        content['save_path'] = request.POST.get('save_path')
        global mewe_save_path
        mewe_save_path = content['save_path']
        content['browser'] = request.POST.get('browser')
        content['browser_data'] = request.POST.get('browser_data')
        os.popen(f'{PYTHON38_PATH} {MEWE_SCRIPT_PATH} {content["email"]} {content["password"]} {content["type"]} {content["type_data"]} {content["interval"]} {content["group"]} {content["save_path"]} {content["browser"]} {content["browser_data"]}')
    return JsonResponse(result)


def mewe_data_port(request):
    # print(f'{mewe_save_path}/state.json')
    if os.path.exists(f'{mewe_save_path}/state.json'):
        try:
            stateF = open(f'{mewe_save_path}/state.json', 'r', encoding='utf-8')
            content = json.load(stateF)
            stateF.close()
            content['returnCode'] = True
        except Exception as e:
            content = {'returnCode': False}
        return JsonResponse(content)
    else:
        return JsonResponse({'returnCode': False})


def line_port(request):
    content = {
        'email': '',
        'password': '',
        'type': '',  # t i
        'type_data': '',
        'interval': '',
        'save_path': '',
        'browser': '',
        'browser_data': '',
    }
    result = {'returnCode': True,
              }
    if request.method == 'POST':
        content['email'] = request.POST.get('email')
        content['password'] = request.POST.get('password')
        content['type'] = request.POST.get('type')
        content['type_data'] = request.POST.get('type_data')
        content['interval'] = request.POST.get('interval')
        content['save_path'] = request.POST.get('save_path')
        global line_save_path
        line_save_path = content['save_path']
        content['browser'] = request.POST.get('browser')
        content['browser_data'] = request.POST.get('browser_data')
        os.popen(f'{PYTHON37_PATH} {LINE_SCRIPT_PATH} {content["email"]} {content["password"]} {content["type"]} {content["type_data"]} {content["interval"]} {content["save_path"]} {content["browser"]} {content["browser_data"]}')
    return JsonResponse(result)


def line_data_port(request):
    # print(f'{line_save_path}/state.json')
    if os.path.exists(f'{line_save_path}/state.json'):
        try:
            stateF = open(f'{line_save_path}/state.json', 'r', encoding='utf-8')
            content = json.load(stateF)
            stateF.close()
            content['returnCode'] = True
        except Exception as e:
            # print(e)
            content = {'returnCode': False}
        return JsonResponse(content)
    else:
        return JsonResponse({'returnCode': False})
