#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    from django.conf import settings
    ARIAL_TTF = os.path.join(settings.FONTS_DIR, "arial.ttf")
except ImportError:
    ARIAL_TTF = "arial.ttf"

from PIL import Image, ImageDraw, ImageFont, ImageChops

import six

ARIAL = settings.FONTS_DIR


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def add_margin(im):
    width, height = im.size
    nwidth, nheight = width + 1, height + 1

    new_im = Image.new("RGB", (nwidth, nheight), (232, 232, 232))
    new_im.paste(im, ((nwidth - width)/2, (nheight - height)/2))

    return new_im


def render(txt, fontsize=20, encoding=None):
    txt = txt.strip()
    lines = len(txt.splitlines()) or 1

    font = ImageFont.truetype(ARIAL_TTF, fontsize)
    width, height = font.getsize(txt)

    image = Image.new("RGBA", (width, height*lines), (232,232,232))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), txt, (0, 0, 0), font=font)

    image = trim(image)
    image = add_margin(image)

    buff = six.StringIO()
    image.save(buff, 'png')
    if encoding:
        return buff.getvalue().encode(encoding)
    return buff.get_value()
