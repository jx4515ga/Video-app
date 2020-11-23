from urllib import parse
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import query_utils

#Class to add name, url, and notes, with a length 
class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True)
    video_id = models.CharField(max_length=40, unique=True)


    # Saving the video into the app and displaying in the video list
    def save(self, *args, **kwargs):
        # extract the video id from youtube url
        url_components = parse.urlparse(self.url)

        # Validation for the link "https"
        if url_components.scheme != 'https':
            raise ValidationError(f'Not a Youtube URL {self.url}')
        
         # Validation for the link "www.youtube.com"
        if url_components.netloc != 'www.youtube.com':
            raise ValidationError(f'Not a Youtube URL {self.url}')

         # Validation for the link "/watch"
        if url_components.path != '/watch':
            raise ValidationError(f'Not a Youtube URL {self.url}')

        query_string = url_components.query
        if not query_string:
            raise ValidationError(F'Invalid Youtube URL{self.url}')

        parameters = parse.parse_qs(query_string, strict_parsing=True)
        v_parameters_list = parameters.get('v') # No Key found on the url
        if not v_parameters_list: # checking if none or empty list
            raise ValidationError(f'Invalid Youtube URL, missing parameters {self.url}')
        self.video_id = v_parameters_list[0]

        super().save(*args, **kwargs)

    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Video_ID: {self.video_id}, Notes: {self.notes[:200]}'

    

