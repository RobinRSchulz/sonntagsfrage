#!/bin/sh
echo "Adding cron job"
crontab -l | { cat; echo "5 * * * * python3 /app/getData.py > /app/getDataCron.log"; } | crontab -
