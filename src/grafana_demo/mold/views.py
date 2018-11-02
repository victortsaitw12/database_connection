from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import calendar
from datetime import datetime
from . import models
# Create your views here.

@csrf_exempt
def render(request):
    return JsonResponse([{
        "target": "entries",
        "datapoints": [
            [1.0, 1311836008],
            [2.0, 1311836009],
            [3.0, 1311836010],
            [5.0, 1311836011],
            [6.0, 1311836012]
        ]
    }], safe=False)


@csrf_exempt
def search(request):
    print('===call search===')
    print(request.body)
    data = ["upper_25","upper_50","upper_75","upper_90","upper_95"]
    return JsonResponse(data, safe=False)


@csrf_exempt
def query(request):
    d = datetime.utcnow()
    ts = calendar.timegm(d.utctimetuple())
    print('===call query===%s' % ts)
    print(request.body)

    data = []
    bad_materials = models.badMaterials()
    for key, value in bad_materials.items():
        target = {
            "target": key,
            "datapoints":[
                [value, ts]
            ]
        }
        data.append(target)
    print(data)
    return JsonResponse(data, safe=False)

    data = [
        {
            "target":"upper_75",
            "datapoints":[
                [622, ts],
                [365, ts]
            ]
        },
        {
            "target":"upper_90",
            "datapoints":[
                [861, ts],
                [767, ts]
            ]
        }
    ]



@csrf_exempt
def index(request):
    print('===call index===')
    print(request)
    return HttpResponse(status=200)
