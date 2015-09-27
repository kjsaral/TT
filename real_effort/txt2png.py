#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont, ImageChops

import six


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def add_margin(im):
    width, height = im.size
    nwidth, nheight = map(lambda v: int(round(v * 1.1)), (width, height))

    new_im = Image.new("RGB", (nwidth, nheight), (255, 255, 255))
    new_im.paste(im, ((nwidth - width)/2, (nheight - height)/2))

    return new_im


def render(txt, fontsize=20):
    txt = txt.strip()
    lines = len(txt.splitlines()) or 1

    font = ImageFont.truetype("arial.ttf", fontsize)
    width, height = font.getsize(txt)

    image = Image.new("RGBA", (width, height*lines), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), txt, (0, 0, 0), font=font)

    image = trim(image)
    image = add_margin(image)

    buff = six.StringIO()
    image.save(buff, 'png')
    return buff.getvalue()
