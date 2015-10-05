#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import urls

from otree.default_urls import *

from .models import Constants
from .views import NewTranscriptionAjax


urlpatterns += urls.patterns('',
    urls.url(
        r'^{}/NewTranscriptionAjax/$'.format(Constants.name_in_url),
        NewTranscriptionAjax.as_view(),
        name='{}:NewTranscriptionAjax'.format(Constants.name_in_url)),
)
