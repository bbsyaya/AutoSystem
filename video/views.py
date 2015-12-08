from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from video.models import Video

def _video_params(request, video_id):

    width = request.GET.get("width", "70%")
    height = request.GET.get("height", "350")
    origin = request.get_host()

    return {"video_id": video_id, "origin": origin, "width": width, "height": height}

def video_list(request, username=None):
    """
    list of videos of a user
    if username does not set, shows the currently logged in user
    """

    # If user is not authenticated and username is None, raise an error
    if username is None and not request.user.is_authenticated():
        from django.http import Http404
        raise Http404

    from django.contrib.auth.models import User
    user = User.objects.get(username=username) if username else request.user

    # loop through the videos of the user
    videos = Video.objects.filter(user=user).all()
    video_params = []
    for video in videos:
        video_params.append(_video_params(request, video.video_id))

    return render_to_response(
        "django_youtube/videos.html",
        {"video_params": video_params},
        context_instance=RequestContext(request)
    )