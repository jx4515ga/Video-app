from video_collection.forms import VideoForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower
from .forms import VideoForm, SearchForm
from .models import Video

def home(request):
    app_name = 'Favorite Music Videos' # this is my music category
    return render(request, 'video_collection/home.html', {'app_name': app_name})

# Adding video to the app and post in the app 
def add(request):
    if request.method == "POST":
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            try:
                new_video_form.save()
                return redirect('video_list')
                #messages.info(request, 'New video Saved')
            except ValidationError:
            # show success mesage and list of video
                messages.warning(request, 'Invalid Youtube URL')
            except IntegrityError:
                messages.warning(request, 'You already added the Video.')

        
        messages.warning(request, 'Please check the data entered.')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

    new_video_form = VideoForm() # adding a new video
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form}) 


# Videos will be addedto the list after added
def video_list(request):
    search_form = SearchForm(request.GET)

    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name'))

    else:
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name'))

    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form})