#!/usr/bin/bash

export FLASK_APP=scripts/probebadge/probeflask.py
export FLASK_ENV=development
flask run -p 80
