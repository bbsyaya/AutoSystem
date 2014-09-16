# coding=utf-8
from django.shortcuts import render, render_to_response

# Create your views here.
def article_view(request, article_id):
    return None


def test_view(request):
    # 运行的function

    return render_to_response('result.html', {'list': 1})