# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json
from django.conf import settings

from ._builtin import Page, WaitPage

from . import models
from .models import Constants
from .txtutils import text_is_close_enough


# =============================================================================
# FOR ALL TEMPLATES
# =============================================================================

def vars_for_all_templates(self):
    return {}


# =============================================================================
# BASE CLASS FOR TRAINING
# =============================================================================

class TrainingBase(Page):

    template_name = 'real_effort/Transcription.html'

    form_model = models.Player
    form_fields = []
    text_data = None

    def vars_for_template(self):
        return {
            "png": self.text_data.png,
            "transcription_title": "Training #{}".format(self.text_data.idx),
        }

    def error_message(self, values):
        field_name = self.form_fields[0]

        text_user = values[field_name]
        is_close_enough, distance = text_is_close_enough(
            text_user, self.text_data.text, Constants.dtol)

        intents_fieldname = "training_intents_{}".format(self.text_data.idx)
        intents = (getattr(self.player, intents_fieldname) or 0) + 1
        setattr(self.player, intents_fieldname, intents)

        if is_close_enough:
            distance_fieldname = "training_distance_{}".format(self.text_data.idx)
            setattr(self.player, distance_fieldname, distance)
        elif tol == 0.0:
            return Constants.transcription_error_0
        else:
            return Constants.transcription_error_positive

    def is_displayed(self):
        return self.subsession.round_number == 1


# =============================================================================
# DINAMIC CREATION OF TRAINING PAGES
# =============================================================================

test_pages = []

for rtext in Constants.reference_texts:
    env = locals()

    class_name = "Training{}".format(rtext.idx)

    fieldname = "training_{}".format(rtext.idx)
    attrs = {
        "form_fields": [fieldname],
        "text_data": rtext}

    cls = type(class_name, (TrainingBase,), attrs)
    env[class_name] = cls
    test_pages.append(cls)


# =============================================================================
# REAL PAGES ITSELF
# =============================================================================

class Transcription(Page):

    template_name = 'real_effort/Transcription.html'

    form_model = models.Player
    form_fields = ["transcripted_text"]

    def vars_for_template(self):
        title = "Transcription #{}".format(self.subsession.round_number),
        return {
            "png": self.player.png,
            "transcription_title": title,
        }

    def transcripted_text_error_message(self, value):
        is_close_enough, distance = text_is_close_enough(
            value, self.player.transcription_text, Constants.dtol)
        self.player.text_intents = (self.player.text_intents or 0) + 1
        if is_close_enough:
            self.player.text_distance = distance
        elif tol == 0.0:
            return Constants.transcription_error_0
        else:
            return Constants.transcription_error_positive


# =============================================================================
# PAGE SECUENCE
# =============================================================================

page_sequence = test_pages + [Transcription]
