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

    png_encoding = "base64"
    player_types = [1, 2, 3, 4]
    pt1, pt2, pt3, pt4 = player_types

    random_string_conf = {"numbers": 5, "letters": 15, "spaces": 5}
    number_of_trainings = 10

    # error in case participant is not allowed to make any errors
    transcription_error_0 = "The transcription should be exactly the same as on the image."
    # error in case participant is allowed to make some errors, but not too many
    transcription_error_positive = "This transcription appears to contain too many errors."

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


class Subsession(otree.models.BaseSubsession):

    def before_session_starts(self):
        re_type = self.session.config['player_type']
        for player in self.get_players():
            player.player_re_type = re_type
            player.transcription_text = txtutils.random_string(
                **Constants.random_string_conf)


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

    transcription_text = models.TextField()
    transcripted_text = models.TextField()
    text_distance = models.FloatField()
    text_intents = models.PositiveIntegerField()

    skip_training = models.BooleanField(default=False, widget=widgets.HiddenInput())
    for rtext in Constants.reference_texts:
        env = locals()
        env["training_{}".format(rtext.idx)] = models.TextField(null=True)
        env["training_distance_{}".format(rtext.idx)] = models.FloatField()
        env["training_intents_{}".format(rtext.idx)] = models.PositiveIntegerField()

    def set_payoff(self):
        self.payoff = 0

    @property
    def png(self):
        if not hasattr(self, "__png"):
            self.__png = txt2png.render(
                self.transcription_text, encoding=constants.png_encoding)
        return self.__png

