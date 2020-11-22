from django.test import TestCase
from django.test import testcases
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from .models import Video

class TestHomePageMessage(TestCase):
    def test_app_title_message_shown_on_home_page(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'Favorite Music Videos')

class TestAddVideos(TestCase):
    def test_add_video(self):
        valid_video = {
            'name' : 'What I have Done',
            'url': 'https://www.youtube.com/watch?v=_c1w056MItU',
            'notes' : 'Linking Park'
        }

        url = reverse('add_video')
        response = self.client.post(url, data=valid_video, follow=True)

        self.assertTemplateUsed('video_collection/video_list.html')

        self.assertContains(response, 'What I have Done')
        self.assertContains(response, 'Linking Park')
        self.assertContains(response, 'https://www.youtube.com/watch?v=_c1w056MItU')

        video_count = Video.objects.count()
        self.assertEqual(1, video_count)

        video = Video.objects.first()
        self.assertEqual('What I have Done', video.name)
        self.assertEqual('https://www.youtube.com/watch?v=_c1w056MItU', video.url)
        self.assertEqual('Linking Park', video.notes)
        self.assertEqual('_c1w056MItU', video.video_id)




    def test_add_video_invalid_url_not_added(self):
        invalid_video_urls = [
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?v',
            'https://www.youtube.com/watch?v=',
            'https://www.youtube.com/watch?v=hg76765', 
            'https://github.com',
            'https://minneapolis.edu',

        ]
        for invalid_video_url in invalid_video_urls:
            new_video = {
                'name' : 'What I have Done',
                'url': 'invalid_url',
                'notes' : 'Linking Park'
            }
            url = reverse('add_video')
            response = self.client.post(url, new_video)

            self.assertTemplateNotUsed('video_collection/add.html')

            messages = response.context['messages']
            message_texts = [message.message for message in messages ]

            self.assertIn('Invalid Youtube URL', message_texts)
            self.assertIn('Please check the data entered.', message_texts)

            video_count = Video.objects.count()
            self.assertEqual(0, video_count)

        

class TestVideoList(TestCase):
    def test_all_displayed_in_correct_order(self):

        v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='abc', notes='example', url='https://www.youtube.com/watch?v=124')
        v3 = Video.objects.create(name='AAA', notes='example', url='https://www.youtube.com/watch?v=125')
        v4 = Video.objects.create(name='LMNop', notes='example', url='https://www.youtube.com/watch?v=126')
        
        expected_video_order = [v3, v2, v4, v1]

        url = reverse('video_list')
        response = self.client.get(url)

        videos_in_template = list(response.context['videos'])

        self.assertEqual(videos_in_template, expected_video_order)


    def test_no_videos_message(self):
        url = reverse('video_list')
        response = self.client.get(url)

        self.assertContains(response, 'No videos')
        self.assertEqual(0, len(response.context['videos']))



    def test_video_number_message_one_video(self):
        v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
        url = reverse('video_list')
        response = self.client.get(url)

        self.assertContains(response, '1 video')
        self.assertNotContains(response, '1 videos')


    def test_video_number_message_two_video(self):
        v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=125')
        url = reverse('video_list')
        response = self.client.get(url)

        self.assertContains(response, '2 videos')
        

class TestVideoSearch(TestCase):
    pass

class TestVideoModel(TestCase):

    def test_invalid_url_raises_validation_error(self):
        invalid_video_urls = [
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?v',
            'https://www.youtube.com/watch?v=',
            'https://www.youtube.com/watch?v=hg76765', 
            'https://github.com',
            'https://minneapolis.edu',

        ]
        for invalid_video_url in invalid_video_urls:
            with self.assertRaises(ValidationError):
                Video.objects.create(name='example', url=invalid_video_url, notes='exaple note')
        self.assertEqual(0, Video.objects.count())



    
    def test_duplicate_video_raises_integrity_error(self):
        v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
        with self.assertRaises(IntegrityError):
            Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')