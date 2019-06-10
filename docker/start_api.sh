#!/bin/bash 

sleep 10
source /root/.local/share/virtualenvs/britecore-*/bin/activate
echo "<<<<<<<<<< Export LANG to the Env>>>>>>>>>>"

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

echo "<<<<<<<< Database Setup and Migrations Starts >>>>>>>>>"
sleep 20
# Run database migrations
flask db upgrade

# Seed database
flask seed

# sleep 10
echo "<<<<<<< Database Setup and Migrations Complete >>>>>>>>>>"
echo " "

sleep 5
echo "<<<<<<<<<<<<<<<<<<<< START API >>>>>>>>>>>>>>>>>>>>>>>>"

# Start the API with gunicorn
gunicorn --access-logfile '-' --workers 2 -t 3600 manage:app -b 0.0.0.0:5000 --reload