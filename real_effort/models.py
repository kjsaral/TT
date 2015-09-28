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

from real_effort import training_texts, txt2png

doc = """
This is a task that requires real effort from participants. Subjects are shown
two images of incomprehensible text. Subjects are required to transcribe (copy)
the text into a text entry field. The quality of a subject's transcription is
measured by the
<a href="http://en.wikipedia.org/wiki/Levenshtein_distance">Levenshtein distance</a>.
"""

class Constants(otree.constants.BaseConstants):

    name_in_url = 'real_effort'
    players_per_group = None
    num_rounds = 1

    dtol = 0.0

    player_types = [1, 2, 3, 4]
    pt1, pt2, pt3, pt4 = player_types

    # error in case participant is not allowed to make any errors
    transcription_error_0 = "The transcription should be exactly the same as on the image."
    # error in case participant is allowed to make some errors, but not too many
    transcription_error_positive = "This transcription appears to contain too many errors."

    reference_texts = [
        (idx+1, data[0] or dtol, data[1], txt2png.render(data[1]))
        for idx, data in enumerate(training_texts.TEXTS)]



class Subsession(otree.models.BaseSubsession):

    player_type = models.IntegerField(min=min(Constants.player_types),
                                      max=max(Constants.player_types))

    def before_session_starts(self):
        if self.round_number == 1:
            self.player_type = self.session.config['player_type']


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    for idx, tol, text, png in Constants.reference_texts:
        Player = locals()
        Player["training_{}".format(idx)] = models.TextField()
        Player["training_distance_{}".format(idx)] = models.FloatField()
        Player["training_intents_{}".format(idx)] = models.PositiveIntegerField()

    def set_payoff(self):
        self.payoff = 0

