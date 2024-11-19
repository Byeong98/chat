from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class AccountsAPIView(APIView):

    def get(self, request):
        return Response({"accounts": "1"})