# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


class Question(Page):

    form_model = models.Player
    form_fields = ["name", "age", "email", "gender", "major",
                   "location_of_your_partners_influence_your_decisions",
                   "working_in_a_location_of_their_choice_more_less_to_the_team",
                   "partners_in_location_their_choice_worked_harder_than_the_lab",
                   "I_work_best_in", "risks_in_everyday_life", "risks_in_financial_decision"]


page_sequence = [Question]
