#!/bin/bash
mkdir -p /var/run/apache2
chown -R www-data:www-data /app
. /etc/apache2/envvars
cron
sleep 1
exec apache2 -DFOREGROUND