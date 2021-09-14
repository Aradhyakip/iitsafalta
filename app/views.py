from json.decoder import JSONDecodeError
from .models import JSONPOSTRequest, HTTPGETRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from json import loads, dumps
from requests import post, get
from urllib.parse import urlparse
from ast import literal_eval

IITSAFALTA_BYPASS = {
    "storeUserActivity": {'message': 'Success', 'flag': 'Y'},
    "storeVideoActivity": {'message': 'Success', 'flag': 'Y'},
    "parentActivity": {'message': 'Success', 'flag': 'Y'},
    "checkSubscriptionValidity": {"message": "Subscribed", "flag": "N"},
}


def dashboard_handler(response_body: dict):
    json = response_body
    json['records']['subjects'] = [
        {
            "subject_id": "1",
            "subject_name": "XII_Physics",
            "display_name": "12 P",
            "dashboard_icon": "ntse/images/mat.png",
            "icon": "https://s3.ap-south-1.amazonaws.com/static.elements.ntseguru/subsubject_thumb/ic_physics.svg"
        },
        {
            "subject_id": "2",
            "subject_name": "XII_Chemistry",
            "display_name": "12 C",
            "dashboard_icon": "ntse/images/lab.png",
            "icon": "https://s3.ap-south-1.amazonaws.com/static.elements.ntseguru/subsubject_thumb/ic_chemistry.svg"
        },
        {
            "subject_id": "3",
            "subject_name": "XII_Mathematics",
            "display_name": "12 M",
            "dashboard_icon": "ntse/images/mathematics.png",
            "icon": "https://s3.ap-south-1.amazonaws.com/static.elements.ntseguru/subsubject_thumb/ic_maths.svg"
        },
        {
            "subject_id": "4",
            "subject_name": "XI_Physics",
            "display_name": "11 P",
            "dashboard_icon": "ntse/images/mat.png",
            "icon": "https://s3.ap-south-1.amazonaws.com/static.elements.ntseguru/subsubject_thumb/ic_physics.svg"
        },
        {
            "subject_id": "5",
            "subject_name": "XI_Chemistry",
            "display_name": "11 C",
            "dashboard_icon": "ntse/images/lab.png",
            "icon": "https://s3.ap-south-1.amazonaws.com/static.elements.ntseguru/subsubject_thumb/ic_chemistry.svg"
        },
        {
            "subject_id": "6",
            "subject_name": "XI_Mathematics",
            "display_name": "11 M",
            "dashboard_icon": "ntse/images/mathematics.png",
            "icon": "https://s3.ap-south-1.amazonaws.com/static.elements.ntseguru/subsubject_thumb/ic_maths.svg"
        },
        {
            "subject_id": "8",
            "subject_name": "XII_BIOLOGY",
            "display_name": "12 B",
            "dashboard_icon": "ntse/images/biology.png",
            "icon": "https://s3.ap-south-1.amazonaws.com/static.elements.ntseguru/subsubject_thumb/ic_biology.svg"
        },
        {
            "subject_id": "7",
            "subject_name": "XI_BIOLOGY",
            "display_name": "11 B",
            "dashboard_icon": "ntse/images/biology.png",
            "icon": "https://s3.ap-south-1.amazonaws.com/static.elements.ntseguru/subsubject_thumb/ic_biology.svg"
        },
        {
            "subject_id": "9",
            "subject_name": "XI_KVPY",
            "display_name": "KVPY",
            "dashboard_icon": "ntse/images/KVPY.png",
            "icon": "https://s3.ap-south-1.amazonaws.com/static.elements.ntseguru/subsubject_thumb/KVPY+1.svg"
        },
        {
            "subject_id": "10",
            "subject_name": "W_Physics",
            "display_name": "W P",
            "dashboard_icon": "ntse/images/mat.png",
            "icon": "https://s3.ap-south-1.amazonaws.com/static.elements.ntseguru/subsubject_thumb/ic_physics.svg"
        },
        {
            "subject_id": "11",
            "subject_name": "W_Chemistry",
            "display_name": "W C",
            "dashboard_icon": "ntse/images/lab.png",
            "icon": "https://s3.ap-south-1.amazonaws.com/static.elements.ntseguru/subsubject_thumb/ic_chemistry.svg"
        },
        {
            "subject_id": "12",
            "subject_name": "W_Mathematics",
            "display_name": "W M",
            "dashboard_icon": "ntse/images/mathematics.png",
            "icon": "https://s3.ap-south-1.amazonaws.com/static.elements.ntseguru/subsubject_thumb/ic_maths.svg"
        },
        {
            "subject_id": "13",
            "subject_name": "W_BIOLOGY",
            "display_name": "W B",
            "dashboard_icon": "ntse/images/biology.png",
            "icon": "https://s3.ap-south-1.amazonaws.com/static.elements.ntseguru/subsubject_thumb/ic_biology.svg"
        },
    ]

    patched_json = loads(dumps(json).replace('"no"', '"yes"'))
    return patched_json

def get_class_list(response_body: dict):
    json = {
        "message":"Success",
        "flag":"Y",
        "records": [
            {
                "class_id":"1",
                "class_name":"XI Class"
            },
            {
                "class_id":"2",
                "class_name":"XII Class"
            },
            {
                "class_id":"3",
                "class_name":"Dropper"
            },
            {
                "class_id":"4",
                "class_name":"XI Optimizer"
            }
        ]
    }
    return json

def subscribed_inject(response_body: dict):
    return loads(dumps(response_body).replace('"no"', '"yes"'))

def paid_inject(response_body: dict):
    return loads(dumps(response_body).replace('"paid"', '"free"'))

IITSAFALTA_INJECT = {
    "getDashboard": dashboard_handler,
    "getClassList":get_class_list,
    "getChapters":subscribed_inject,
    "getVideoList":subscribed_inject,
    "getSMTopics": paid_inject
}


@csrf_exempt
def iitsafalta(request: HttpRequest, version: int, endpoint: str) -> JsonResponse:
    # Assume Request is POST
    # Incase of a empty request
    request_body = b"{}"
    if len(request.body) != 0:
        request_body = request.body

    if endpoint in IITSAFALTA_BYPASS:
        JSONPOSTRequest(
            url=f"https://iitsafalta.in/apis_android/api_{version}/iitsafalta/{endpoint}",
            headers=dict(request.headers),
            sent_data=loads(request_body.decode('utf-8')),
            received_data=IITSAFALTA_BYPASS[endpoint]
        ).save()
        return JsonResponse(IITSAFALTA_BYPASS[endpoint])

    # Modifying Host because of the Reverse Proxy running on AWS for IIT Safalta.
    __head = dict(request.headers)
    __head['Host'] = 'iitsafalta.in'
    # __head['x-api-key'] = "Guru#Kul@m4404"

    resp = post(url=f"https://iitsafalta.in/apis_android/api_{version}/iitsafalta/{endpoint}",
                json=loads(request_body.decode('utf-8')),
                auth=('admin', '1234'),
                headers=__head
                )

    json = resp.json()
    if endpoint in IITSAFALTA_INJECT:
        json = IITSAFALTA_INJECT[endpoint](json)

    JSONPOSTRequest(
        url=f"https://iitsafalta.in/apis_android/api_{version}/iitsafalta/{endpoint}",
        headers=dict(request.headers),
        sent_data=loads(request_body.decode('utf-8')),
        received_data=json
    ).save()

    return JsonResponse(json)


@csrf_exempt
def generic(request, url: str):
    if request.method == "GET":
        HTTPGETRequest(
            url=url,
            headers=dict(request.headers),
        ).save()
        return HttpResponse(get(url).content)
    # Method is most probably post
    __head = dict(request.headers)
    __head['Host'] = urlparse(url).netloc

    resp = post(url=url,
                data=request.body.decode('utf-8'),
                headers=__head
                )
    json = {"raw": resp.content.decode('utf-8')}
    try:
        json['parsed'] = loads(resp.content.decode('utf-8'))
    except JSONDecodeError:
        pass

    # This saves
    JSONPOSTRequest(
        url=url,
        headers=dict(request.headers),
        sent_data={"raw": request.body.decode('utf-8')},
        received_data=json
    ).save()
    return HttpResponse(resp.content)


def export_http_requests(request):
    data = list(HTTPGETRequest.objects.values())
    return JsonResponse({'data': data})


def export_json_requests(request):
    data = list(JSONPOSTRequest.objects.values())
    return JsonResponse({'data': data})
