#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import random

import six

def levenshtein(a, b):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j-1] + 1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]


def text_is_close_enough(
    text_user, text_reference, max_error_rate, ignore_case=True):
        if ignore_case:
            text_user = text_user.lower()
            text_reference = text_reference.lower()
        error_threshold = len(text_reference) * max_error_rate
        distance = levenshtein(text_user, text_reference)
        return distance <= error_threshold, distance


def random_string(numbers, letters, spaces):
    numbers = [random.choice(string.digits) for _ in six.moves.range(numbers)]
    letters = [random.choice(string.ascii_uppercase) for _ in six.moves.range(letters)]
    spaces = [" "] * spaces
    rstring = numbers + letters + spaces
    random.shuffle(rstring)
    return " ".join("".join(rstring).strip().split())
