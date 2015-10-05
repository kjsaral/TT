# -*- coding: utf-8 -*-
from __future__ import division

from django.utils import timezone

from django.http import JsonResponse
from django.views.generic import View

from otree.common import Currency as c, currency_range, safe_json
from django.conf import settings

from ._builtin import Page, WaitPage

from . import models
from .models import Constants
from .libs.txtutils import text_is_close_enough


# =============================================================================
# FOR ALL TEMPLATES
# =============================================================================

def vars_for_all_templates(self):
    return {}


# =============================================================================
# BASE CLASS FOR TRAINING
# =============================================================================

class TrainingBase(Page):

    template_name = 'real_effort/TranscriptionTraining.html'

    form_model = models.Player
    form_fields = []
    text_data = None

    def vars_for_template(self):
        return {
            "png": self.text_data.png,
            "transcription_title": "Training #{}".format(self.text_data.idx),
            "text_fieldname": self.form_fields[0]}

    def error_message(self, values):
        field_name, skip_fieldname = self.form_fields

        skip = values[skip_fieldname]
        if skip:
            return

        text_user = values[field_name]
        is_close_enough, distance = text_is_close_enough(
            text_user, self.text_data.text, Constants.dtol)

        intents_fieldname = "training_intents_{}".format(self.text_data.idx)
        intents = (getattr(self.player, intents_fieldname) or 0) + 1
        setattr(self.player, intents_fieldname, intents)

        if is_close_enough:
            pass
        elif Constants.dtol == 0.0:
            return Constants.transcription_error_0
        else:
            return Constants.transcription_error_positive

    def is_displayed(self):
        return self.subsession.round_number == 1 and not self.player.skip_training


# =============================================================================
# DINAMIC CREATION OF TRAINING PAGES
# =============================================================================

test_pages = []

for rtext in Constants.reference_texts:
    env = locals()

    class_name = "Training{}".format(rtext.idx)

    fieldname = "training_{}".format(rtext.idx)
    attrs = {
        "form_fields": [fieldname, "skip_training"],
        "text_data": rtext}

    cls = type(class_name, (TrainingBase,), attrs)
    env[class_name] = cls
    test_pages.append(cls)


# =============================================================================
# REAL PAGES ITSELF
# =============================================================================

class Introduction(Page):
    pass


class BeforeRound1(Page):

    def vars_for_template(self):
        return {
            "time_limit": int(Constants.round_1_seconds / 60)}

    def before_next_page(self):
        self.player.round_1_start_time = timezone.now()


class Round1(Page):

    form_model = models.Player
    form_fields = ["transcription"]

    def vars_for_template(self):
        idx = self.player.round_1_idx
        return {
            "idx": idx,
            "correct_answers": idx,
            "time_left": self.player.round_1_time_left(),
            "intents": self.player.round_1_intents[idx],
            "text": self.player.round_1_transcription_texts[idx],
            "png": self.player.round_1_png(idx)}

    def transcription_error_message(self, value):
        if not self.player.round_1_time_left():
            return

        idx = self.player.round_1_idx
        text_reference = self.player.round_1_transcription_texts[idx]
        self.player.round_1_intents[idx] += 1

        is_close_enough, distance = text_is_close_enough(
            value, text_reference, Constants.dtol)

        if is_close_enough:
            self.player.round_1_idx = idx + 1
        elif Constants.dtol == 0.0:
            return Constants.transcription_error_0
        else:
            return Constants.transcription_error_positive

        if self.player.round_1_idx < Constants.transcriptions_limit:
            return "----"

    def before_next_page(self):
        self.player.set_round_1_a_payoff()

    def is_displayed(self):
        return self.player.round_1_time_left()


class ResultsRound1(Page):

    def vars_for_template(self):
        return {
            "correct_answers": self.player.round_1_idx,
            "earnings": self.player.round_1_a_payoff
        }


# =============================================================================
# PAGE SECUENCE
# =============================================================================

page_sequence = (
    [Introduction] + test_pages +
    [BeforeRound1, Round1, ResultsRound1]
)
