#!/bin/bash

zip -r anki-forvodl-anki21.zip * \
    -x meta.json \
    -x \*.gitignore \
    -x \*forvo-button-copyrighted.png \
    -x package.sh
