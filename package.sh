#!/bin/bash

zip -r anki-forvodl-anki21.ankiaddon * \
    -x meta.json \
    -x \*.gitignore \
    -x \*forvo-button-copyrighted.png \
    -x package.sh \
    -x __pycache__/\*
