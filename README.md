# dashboard #

### Repository for home dashboard. ###

The project is split in two parts: 
 - Dashboard visualizations
 - Web application that will be used to view the dashboard


The goal is to create a dashboard for home usage that will include the following parts (still in consideration):

Somewhat ready:
1. Bus schedule screen, which will show the arriving busses on the three nearest bus stops and for how long it will take from them to arrive at the stop. - Made using Tampere's public transport API
- Files: bus_data_to_database.py, bus_schedule_visualization.py
2. Outdoor temperature/forecast - Made using weatherbit.io-api
- Files: weather_forecast_to_database.py

Still to do:
3. News feed - Data will be taken from YLE-API
4. Indoor temperature/humidity monitor. The values will be measured using Raspberry Pi Sense HAT.

The dashboard implementation is made using Python as the language and PostgreSQL as a database.

The web application is made using Django web framework in Python. The files are located in "dassikka"-directory.
Web-application includes: Registration, login, logout, editing profile information, homepage, dashboard-page.
