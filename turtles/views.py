from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
# login/views.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Turtle
from django.contrib.auth.hashers import make_password, check_password

from .serializers import TurtleSerializer

# 거북이 가져오기
@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def turtles(request):
    user_email = request.query_params.get('user_email', "")
    user = Turtle.objects.filter(email=user_email).first()
    if request.method == 'GET':
        selrialize = TurtleSerializer(user)
        return Response(selrialize.data)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serial = TurtleSerializer(user, data=data)

        if serial.is_valid(raise_exception=True):
            serial.save()
            return JsonResponse(serial.data, status=201)
        return JsonResponse(serial.errors, status=400)

    if request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)

# 사용자 거북이 생성
class CreateTurtle(APIView):
    def post(self, request):
        post_data = {
            "email": request.data.get("email"),
            "name": request.data.get("name"),
            "num": request.data.get("num"),
            "ease": request.data.get("ease"),
            "best": request.data.get("best"),
        }
        serializer = TurtleSerializer(post_data)
        print(request.data)
        if Turtle.objects.filter(email=request.data.get('email','')).exists():
            # DB에 있는 값 출력할 때 어떻게 나오는지 보려고 user 객체에 담음
            user = Turtle.objects.get(email=request.data.get('email',''))
            data = {
                "email": user.email,
                "name": user.name,
                "num": user.num,
                "ease": user.ease,
                "best": user.best,
                "created": user.created,
            }
            return Response(data=TurtleSerializer(data).data)
        turtle = serializer.create(post_data)

        return Response(data=TurtleSerializer(turtle).data)

# 해당 유저와 시작일이 똑같은 유저들 반환
class StartDayTurtles(APIView):
    def get(self, request):
        user_email = request.query_params.get('user_email', "")
        user = Turtle.objects.get(email=user_email)

        turtle = Turtle.objects.filter(created=user.created)
        serializers = TurtleSerializer(turtle, many=True)
        return Response(serializers.data)

@api_view(['GET'])
def tutleList(request):
    allst = Turtle.objects.all()
    serializer = TurtleSerializer(allst, many=True)
    return Response(serializer.data)
