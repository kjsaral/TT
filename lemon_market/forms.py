# -*- coding: utf-8 -*-
import lemon_market.models as models
from lemon_market.utilities import Form


class BidForm(Form):

    class Meta:
        model = models.Match
        fields = ['bid_amount']

    def labels(self):
        return {
            'bid_amount': self.match.bid_amount,
        }

    def labels(self):
        return {'bid_amount': 'Bid Amount'}

    def bid_amount_error_message(self, value):
        if (value < 0) or (value > self.treatment.max_bid_amount):
            return 'Bid Amount should be between {} and {}'.format(0, self.treatment.max_bid_amount)

