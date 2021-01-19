# Copyright (C) 2021 Magenta ApS, http://magenta.dk.
# Contact: info@magenta.dk.
#

################################################################################
# Changes to this file requires approval from Labs. Please add a person from   #
# Labs as required approval to your MR if you have any changes.                #
################################################################################


FROM python:3.8 AS os2borgerpc

LABEL org.opencontainers.image.title="OS2borgerPC" \
      org.opencontainers.image.vendor="Magenta ApS" \
      org.opencontainers.image.licenses="GPL" \
      org.opencontainers.image.url="https://os2.eu/produkt/os2borgerpc"\
      org.opencontainers.image.source="https://github.com/OS2borgerPC/admin-site"

ENV PYTHONUNBUFFERED=1 \
  BPC_SYSTEM_CONFIG_PATH=/code/docker/docker-settings.ini \
  BPC_USER_CONFIG_PATH=/user-settings.ini \
  PYTHONPATH=/code/admin_site/:$PYTHONPATH\
  DJANGO_SETTINGS_MODULE=os2borgerpc_admin.settings


WORKDIR /code/
COPY admin_site/scripts/sys-requirements.txt sys-requirements.txt

# hadolint ignore=DL3008
RUN set -ex \
  # Add a bpc group and user. Note: this is a system user/group, but have
  # UID/GID above the normal SYS_UID_MAX/SYS_GID_MAX of 999, but also above the
  # automatic ranges of UID_MAX/GID_MAX used by useradd/groupadd. See
  # `/etc/login.defs`. Hopefully there will be no conflicts with users of the
  # host system or users of other docker containers.
  && groupadd -g 75030 -r bpc\
  && useradd -u 75030 --no-log-init -r -g bpc bpc \
  # Install system dependencies from file.
  && apt-get -y update \
  && apt-get -y install --no-install-recommends "$(grep -o '^[^#][[:alnum:].-]*' sys-requirements.txt)" \
  # clean up after apt-get and man-pages
  && apt-get clean \
  && rm -rf "/var/lib/apt/lists/*"  "/tmp/*"  "/var/tmp/*"  "/usr/share/man/??"  "/usr/share/man/??_*" \
 # create folders at easily mountable paths for output from django
 && install -o bpc -g bpc -d /log \
 && install -o bpc -g bpc -d /static \
 && install -o bpc -g bpc -d /code/admin_site/site_media/script_uploads \
 && install -o bpc -g bpc -d /code/admin_site/site_media/parameter_uploads \
 && install -o bpc -g bpc -d /code/admin_site/site_media/images

VOLUME /log
VOLUME /static
VOLUME /code/admin_site/site_media/script_uploads
VOLUME /code/admin_site/site_media/parameter_uploads
VOLUME /code/admin_site/site_media/images


# Install requirements.
COPY admin_site/scripts/requirements.txt /code/admin_site/scripts/requirements.txt
RUN pip3 install --no-cache-dir -r  admin_site/scripts/requirements.txt

# Copy backend code.
COPY README.rst .
COPY LICENSE .
COPY docker ./docker
COPY admin_site ./admin_site

# Run the server as the bpc user on port 9999

WORKDIR /code/admin_site
USER bpc:bpc
EXPOSE 9999
ENTRYPOINT ["/code/docker/docker-entrypoint.sh"]
CMD ["gunicorn", \
  "--config", "/code/docker/gunicorn-settings.py", \
  "os2borgerpc_admin.wsgi"]