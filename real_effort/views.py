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
# INTRO
# =============================================================================

class Consent(Page):
    pass


class Introduction(Page):
    pass


class GeneralDescription(Page):
    pass


class TaskDescription(Page):
    pass


# =============================================================================
# TRAINING
# =============================================================================

class TrainingRound(Page):

    form_model = models.Player
    form_fields = ["transcription", "training_skip"]

    def vars_for_template(self):
        idx = self.player.training_idx
        return {
            "idx": idx,
            "idx_p1": idx+1,
            "correct_answers": idx,
            "intents": self.player.training_intents[idx],
            "text": self.player.training_transcription_texts[idx],
            "png": self.player.training_png(idx)}

    def error_message(self, values):
        if values["training_skip"]:
            return

        idx = self.player.training_idx
        text_reference = self.player.training_transcription_texts[idx]
        self.player.training_intents[idx] += 1

        is_close_enough, distance = text_is_close_enough(
            values["transcription"], text_reference, Constants.dtol)

        if is_close_enough:
            self.player.training_idx = idx + 1
        elif Constants.dtol == 0.0:
            return Constants.transcription_error_0
        else:
            return Constants.transcription_error_positive

        if self.player.training_idx < Constants.training_counts:
            return "----"

    def is_displayed(self):
        return (not self.player.training_skip)

    def before_next_page(self):
        self.player.transcription = None


# =============================================================================
# ROUND 1
# =============================================================================

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

    def is_displayed(self):
        return self.player.round_1_time_left()


class ResultsRound1(Page):

    def vars_for_template(self):
        if self.player.round_1_a_payoff is None:
            self.player.set_round_1_payoff()
        return {
            "correct_answers": self.player.round_1_idx,
            "earnings": self.player.round_1_a_payoff
        }


# =============================================================================
# ROUND 2
# =============================================================================

class ChangeInGame(Page):

    def vars_for_template(self):
        return {"minutes": int(Constants.round_2_seconds/60)}


class TaskDescription2(Page):

    def vars_for_template(self):
        return {
            "result_a": 10 * Constants.a_payoff + (50 * Constants.b_payoff) / 3,
            "result_b": 20 * Constants.a_payoff + (40 * Constants.b_payoff) / 3
        }


class MemberInformation(Page):
    pass


class BeforeRound2(Page):

    def vars_for_template(self):
        return {
            "time_limit": int(Constants.round_2_seconds / 60)}

    def before_next_page(self):
        self.player.round_2_start_time = timezone.now()


class Round2(Page):

    form_model = models.Player
    form_fields = ["transcription", "share"]

    def vars_for_template(self):
        idx = self.player.round_2_idx
        count_b = self.player.round_2_shared
        count_a = idx - count_b
        return {
            "idx": idx,
            "correct_answers_a": count_a if count_a > 0 else 0,
            "correct_answers_b": count_b if count_b > 0 else 0,
            "time_left": self.player.round_2_time_left(),
            "intents": self.player.round_2_intents[idx],
            "text": self.player.round_2_transcription_texts[idx],
            "png": self.player.round_2_png(idx)}

    def error_message(self, values):

        if not self.player.round_2_time_left():
            return

        share = values["share"]
        value = values["transcription"]

        idx = self.player.round_2_idx
        text_reference = self.player.round_2_transcription_texts[idx]
        self.player.round_2_intents[idx] += 1

        is_close_enough, distance = text_is_close_enough(
            value, text_reference, Constants.dtol)

        if is_close_enough:
            self.player.round_2_idx = idx + 1
        elif Constants.dtol == 0.0:
            return Constants.transcription_error_0
        else:
            return Constants.transcription_error_positive

        if share:
            self.player.round_2_shared = self.player.round_2_shared + 1

        if self.player.round_2_idx < Constants.transcriptions_limit:
            return "----"

    def is_displayed(self):
        return self.player.round_2_time_left()


class ResultsRound2(Page):

    def vars_for_template(self):
        if self.player.round_2_a_payoff is None or self.player.round_2_b_payoff is None:
            self.player.set_round_2_payoff()
        count_b = self.player.round_2_shared
        count_a = self.player.round_2_idx - count_b
        return {
            "correct_answers_a": count_a if count_a > 0 else 0,
            "correct_answers_b": count_b if count_b > 0 else 0,
            "earnings_a": self.player.round_2_a_payoff,
            "earnings_b": self.player.round_2_b_payoff,
        }


# =============================================================================
# ROUND 3
# =============================================================================

class BeforeRound3(Page):

    def vars_for_template(self):
        return {
            "time_limit": int(Constants.round_3_seconds / 60)}

    def before_next_page(self):
        self.player.round_3_start_time = timezone.now()


class Round3(Page):

    form_model = models.Player
    form_fields = ["transcription", "share"]

    def vars_for_template(self):
        idx = self.player.round_3_idx
        count_b = self.player.round_3_shared
        count_a = idx - count_b
        return {
            "idx": idx,
            "correct_answers_a": count_a if count_a > 0 else 0,
            "correct_answers_b": count_b if count_b > 0 else 0,
            "time_left": self.player.round_3_time_left(),
            "intents": self.player.round_3_intents[idx],
            "text": self.player.round_3_transcription_texts[idx],
            "png": self.player.round_3_png(idx)}

    def error_message(self, values):

        if not self.player.round_3_time_left():
            return

        share = values["share"]
        value = values["transcription"]

        idx = self.player.round_3_idx
        text_reference = self.player.round_3_transcription_texts[idx]
        self.player.round_3_intents[idx] += 1

        is_close_enough, distance = text_is_close_enough(
            value, text_reference, Constants.dtol)

        if is_close_enough:
            self.player.round_3_idx = idx + 1
        elif Constants.dtol == 0.0:
            return Constants.transcription_error_0
        else:
            return Constants.transcription_error_positive

        if share:
            self.player.round_3_shared = self.player.round_3_shared + 1

        if self.player.round_3_idx < Constants.transcriptions_limit:
            return "----"

    def is_displayed(self):
        return self.player.round_3_time_left()


class ResultsRound3(Page):

    def vars_for_template(self):
        if self.player.round_3_a_payoff is None or self.player.round_3_b_payoff is None:
            self.player.set_round_3_payoff()
        count_b = self.player.round_3_shared
        count_a = self.player.round_3_idx - count_b
        return {
            "correct_answers_a": count_a if count_a > 0 else 0,
            "correct_answers_b": count_b if count_b > 0 else 0,
            "earnings_a": self.player.round_3_a_payoff,
            "earnings_b": self.player.round_3_b_payoff,
        }



# =============================================================================
# PAGE SECUENCE
# =============================================================================

page_sequence = [
    Consent, Introduction, GeneralDescription, TaskDescription,
    TrainingRound,
    BeforeRound1, Round1, ResultsRound1,
    ChangeInGame, TaskDescription2, MemberInformation,
    BeforeRound2, Round2, ResultsRound2,
    BeforeRound3, Round3, ResultsRound3
]
