# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
import otree.constants
from otree import widgets
from otree import forms
from otree.common import Currency as c, currency_range
import random
from django.core.validators import MaxLengthValidator
# </standard imports>

from django.utils import timezone

import collections

import six

from .libs import txt2png, txtutils

doc = """
This is a task that requires real effort from participants. Subjects are shown
two images of incomprehensible text. Subjects are required to transcribe (copy)
the text into a text entry field. The quality of a subject's transcription is
measured by the
<a href="http://en.wikipedia.org/wiki/Levenshtein_distance">Levenshtein distance</a>.
"""

ReferenceText = collections.namedtuple("ReferenceText", ["idx", "text", "png"])

class Constants(otree.constants.BaseConstants):

    name_in_url = 'real_effort'
    players_per_group = None
    num_rounds = 1

    dtol = 0.0

    skip_text, timesup_text = "-* Skipped *-", "-* Times Up *-"

    png_encoding = "base64"
    player_types = [1, 2, 3, 4]
    pt1, pt2, pt3, pt4 = player_types

    a_payoff, b_payoff = c("0.10"), c("0.23")

    random_string_conf = {"numbers": 5, "letters": 15, "spaces": 5}

    # 5, 20 and 20 minutes
    round_1_seconds, round_2_seconds, round_3_seconds = 500, 1200, 1200

    # error in case participant is not allowed to make any errors
    transcription_error_0 = "The transcription should be exactly the same as on the image."
    # error in case participant is allowed to make some errors, but not too many
    transcription_error_positive = "This transcription appears to contain too many errors."

    transcriptions_limit = 500

    reference_only_texts = (
        "12M1ZU J2KO ERP H O9DRYA",
        "4C3 J H4 LF UJN8BBTX KPA9",
        "4NOOIZ C8Z3WJ E5Q9Q OGH",
        "75CNBQDHOQ 56KUBCI 9S Q",
        "NG6L 7J4O2A9 NA MHNF SGW",
        "9SP 9P IR7 MDI7OGWHBS2 V",
        "JEA86MGZ S 5Z4COQ3 I BWJ",
        "IJ LD JS QFP 3T3MYS0AY01",
        "PXZ 6LH3OYCDJ A49Q I1UV",
        "A15DS TV0TEC CRYCC8D 9Z")
    reference_texts = [
        ReferenceText(idx=idx+1, text=text,
                      png=txt2png.render(text, encoding=png_encoding))
        for idx, text in enumerate(reference_only_texts)]

    continue_in_the_round = random.random()


class Subsession(otree.models.BaseSubsession):

    def before_session_starts(self):
        re_type = self.session.config['player_type']
        for player in self.get_players():
            player.player_re_type = re_type
            round_1_tt, round_2_tt, round_3_tt, intents = [], [], [], []
            while len(intents) < Constants.transcriptions_limit:
                round_1_tt.append(txtutils.random_string(**Constants.random_string_conf))
                round_2_tt.append(txtutils.random_string(**Constants.random_string_conf))
                round_3_tt.append(txtutils.random_string(**Constants.random_string_conf))
                intents.append(0)
            player.round_1_transcription_texts = round_1_tt
            player.round_2_transcription_texts = round_2_tt
            player.round_3_transcription_texts = round_3_tt
            player.round_1_intents = list(intents)
            player.round_2_intents = list(intents)
            player.round_3_intents = list(intents)


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    player_re_type = models.IntegerField(min=min(Constants.player_types),
                                         max=max(Constants.player_types))

    transcription = models.TextField()

    round_1_start_time = models.DateTimeField()
    round_1_idx = models.PositiveIntegerField(default=0)
    round_1_transcription_texts = models.JSONField()
    round_1_intents = models.JSONField()

    round_2_start_time = models.DateTimeField()
    round_2_idx = models.PositiveIntegerField(default=0)
    round_2_transcription_texts = models.JSONField()
    round_2_intents = models.JSONField()
    round_1_a_payoff = models.CurrencyField()

    round_3_start_time = models.DateTimeField()
    round_3_idx = models.PositiveIntegerField(default=0)
    round_3_transcription_texts = models.JSONField()
    round_3_intents = models.JSONField()

    skip_training = models.BooleanField(default=False, widget=widgets.HiddenInput())
    for rtext in Constants.reference_texts:
        env = locals()
        env["training_{}".format(rtext.idx)] = models.TextField(null=True)
        env["training_intents_{}".format(rtext.idx)] = models.PositiveIntegerField()

    def set_payoff(self):
        self.payoff = 0

    def round_1_png(self, idx):
        if not hasattr(self, "__round_1_png"):
            self.__round_1_png = {}
        if idx not in self.__round_1_png:
            text = self.round_1_transcription_texts[idx]
            self.__round_1_png[idx] = txt2png.render(text, encoding=Constants.png_encoding)
        return self.__round_1_png[idx]

    def set_round_1_a_payoff(self):
        self.round_1_a_payoff = Constants.a_payoff * self.round_1_idx

    def round_1_time_left(self):
        start = self.round_1_start_time
        now = timezone.now()
        time_left = Constants.round_1_seconds - (now - start).seconds
        return time_left if time_left > 0 else 0

    def round_2_png(self, idx):
        if not hasattr(self, "__round_2_png"):
            self.__round_2_png = {}
        if idx not in self.__round_2_png:
            text = self.round_2_transcription_texts[idx]
            self.__round_2_png[idx] = txt2png.render(text, encoding=Constants.png_encoding)
        return self.__round_2_png[idx]

    def round_2_time_left(self):
        start = self.round_2_start_time
        now = timezone.now()
        time_left = Constants.round_2_seconds - (now - start).seconds
        return time_left if time_left > 0 else 0

    def round_3_png(self, idx):
        if not hasattr(self, "__round_3_png"):
            self.__round_3_png = {}
        if idx not in self.__round_3_png:
            text = self.round_3_transcription_texts[idx]
            self.__round_3_png[idx] = txt2png.render(text, encoding=Constants.png_encoding)
        return self.__round_3_png[idx]

    def round_3_time_left(self):
        start = self.round_3_start_time
        now = timezone.now()
        time_left = Constants.round_3_seconds - (now - start).seconds
        return time_left if time_left > 0 else 0
