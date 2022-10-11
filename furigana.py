# anki-forvodl - A half-automatic Forvo downloader addon for Anki
# Copyright (C) 2022 yunidatsu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# This code was adapted from Anki's old file pylib/anki/template/furigana.py,
# which was deleted a while ago. It was probably moved elsewhere, but I'm
# too lazy to search for it, so here goes...

# The purpose of this module is to extract just the kanji or kana part of a
# bracketized string that contains both versions, e.g. "先生[せんせい]". That
# format is used by the "Japanese Support" addon, with things like
# {{kanji:Reading}} and {{kana:Reading}}.


import re

pattern = r" ?([^ >]+?)\[(.+?)\]";


def _replace_func(repl):
    def func(match):
        if match.group(2).startswith("sound:"):
            # This is (probably) a sound string like "[sound:example.mp3]", which
            # is obviously NOT a kanji/kana string.
            return match.group(0)
        else:
            return re.sub(pattern, repl, match.group(0))

    return func


def _preprocess(text):
    return text.replace("&nbsp;", " ")


def kanji(text):
    return re.sub(pattern, _replace_func(r"\1"), _preprocess(text))


def kana(text):
    return re.sub(pattern, _replace_func(r"\2"), _preprocess(text))
