#!/bin/bash

caddy reload
FLASK_APP=main.py FLASK_ENV=development flask run