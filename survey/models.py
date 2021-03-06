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
    players_per_group = None
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
        verbose_name="Are you", max_length=255, widget=widgets.RadioSelect(),
        choices=["Male", "Female"])

    major = models.CharField(max_length=1000, verbose_name="What is your major?")

    working_in_a_location_of_their_choice_more_less_to_the_team = models.CharField(
        verbose_name = "When you were in a group with two TELECOMMUTERS working in a "
                        "location and time of their choice, did you want to give more "
                        "to the group account than when you were partnered "
                        "with two LAB PARTICIPANTS?", max_length=500,widget=widgets.RadioSelect(),
        choices=["More to the Group Account with TELECOMMUTERS", "Less to the Group Account with TELECOMMUTERS", "Didn't Matter"])

    partners_in_location_their_choice_worked_harder_than_the_lab = models.CharField(
               verbose_name = "Do you believe your TELECOMMUTER group members gave more/less/the same to the group "
                        "account than your LAB PARTICIPANT group members?",
                         max_length=500,widget=widgets.RadioSelect(),
        choices=["TELECOMMUTERS gave more", "TELECOMMUTERS gave less", "Both types gave the same"])

    location_of_your_partners_influence_your_decisions = models.TextField(
        verbose_name=("Did your group members' type (TELECOMMUTERS or LAB PARTICIPANTS) "
                      "influence your decisions today in a way not accounted for above? "
                      "If so, please explain."))

    I_work_best_in = models.CharField(
        verbose_name="Which do you prefer working in?", max_length=255, widget=widgets.RadioSelect(),
        choices=["Structured environments", "flexible environments"])

    I_work_prefer = models.CharField(
        verbose_name="Which type of work do you prefer?", max_length=255, widget=widgets.RadioSelect(),
        choices=["Working Alone", "Working in Groups"])

    risks_in_everyday_life = models.PositiveIntegerField(
        min=1, max=10, widget=widgets.SliderInput(),
        verbose_name=("In general, do you take more or less risks in everyday "
                      "life? ('1' = take less risk and '10' take more risk.)"))

    risks_in_financial_decision = models.PositiveIntegerField(
        min=1, max=10, widget=widgets.SliderInput(), default=5,
        verbose_name=(" In general, do you take more or less risks in financial decisions? "
                      "life? ('1' = take less risk and '10' take more risk.)"))

