#!/usr/bin/env python
# -*- coding: utf-8 -*-


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


def text_is_close_enough(text_user, text_reference, max_error_rate):
    error_threshold = len(text_reference) * max_error_rate
    distance = levenshtein(text_user, text_reference)
    return distance <= error_threshold, distance
