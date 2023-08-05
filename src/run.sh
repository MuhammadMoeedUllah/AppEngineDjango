#!/bin/bash

# Start the cloud sql proxy
./cloud_sql_proxy.linux.amd64 -instances="decent-vertex-357610:australia-southeast1:dev-cmt-scanner-db"=tcp:0.0.0.0:5432 -credential_file=/secrets/creds.json & 
  
# Start the second process
exec gunicorn --bind 0.0.0.0:$1 --workers 1 --threads 8 --timeout 0 web.wsgi:application
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?