#!/bin/sh
# Initialize DB (safe to run multiple times)
airflow db init

# Start the scheduler in background
airflow scheduler &

# Start the webserver in foreground (keeps container alive)
exec airflow webserver
