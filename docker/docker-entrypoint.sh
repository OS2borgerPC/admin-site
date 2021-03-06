#!/bin/bash
# Copyright (C) 2019 Magenta ApS, http://magenta.dk.
# Contact: info@magenta.dk.
#
################################################################################
# Changes to this file requires approval from Labs. Please add a person from   #
# Labs as required approval to your MR if you have any changes.                #
################################################################################

set -ex

./manage.py ensure_db_connection --wait 30

if [ "$SKIP_MIGRATIONS" != "yes" ];
then
  # Run Migrate
  python ./manage.py migrate
fi

exec "$@"
