# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>


doc = """
Foo
"""


source_code = ""


bibliography = ()


links = {}


keywords = ()

class Constants:
    name_in_url = 'questionnaire'
    players_per_group = 1
    num_rounds = 1


class Subsession(otree.models.BaseSubsession):
    pass


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    name = models.CharField(max_length=255, verbose_name="Your name")

    age = models.CharField(max_length=255, verbose_name="Your age")

    email = models.EmailField(verbose_name="Your email address")

    gender = models.CharField(
        verbose_name="Are you", max_length=25, widget=widgets.RadioSelect(),
        choices=["Male", "Female"])

    major = models.CharField(max_length=255, verbose_name="What is your major?")




