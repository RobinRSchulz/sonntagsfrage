# Sonntagsfrage-Server
## Description: procedure

* (timestamped) Data is fetched from remote host (periodically e.g. via 
CRON job on 
server) (getData.py)
* server (flask) generates html from template and current data 
(server.py)
* html template is used to visualize the provided data in a fancy way:
  * multi-line graphs
  * etc (todo)

## TODO

* template
* process fetched data in server.py before generating the template.
  * develop data structure for sorted table data 
* use Chart.js 2.9.3 instead of 1.0.2 for colored bars
## debug

* execute getData once
* start server.py
* alter template if necessary
