#!/bin/sh

flask db upgrade

exec gunicon --bind 0.0.0.0:80 "app:create_app()"