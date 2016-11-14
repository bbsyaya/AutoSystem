# coding=utf-8
from django.shortcuts import render, render_to_response

# Create your views here.
from ad.function.taobaoke import import_taobaoke_excel


def import_taobaoke_excel_view(request):
    """
    下载config model中设置好的youtube playlist中的num个视频，并上传到优酷，设置其playlist
    :param request:
    :param num:
    :return:
    """

    result = import_taobaoke_excel()
    if result:
        return render_to_response('result.html', {'text': '下载并上传指定youtube '
                                                          'playlist的视频成功。',
                                                  'dict_items': result})
    else:
        return render_to_response('result.html', {'text': '未下载并上传指定youtube '
                                                          'playlist的视频，情况1：无需下载'})