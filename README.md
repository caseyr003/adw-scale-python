# Python Oracle Autonomous Data Warehouse Scaling Demo

This project is a Python project that scales Oracle Autonomous Data Warehouse based on OCPU utilization.

## Built With

* [Python 3](https://www.python.org/)
* [Docker](https://www.docker.com/)
* [Oracle Autonomous Data Warehouse](https://cloud.oracle.com/en_US/datawarehouse)

## Prerequisites

You will need the following things properly installed on your computer:

* [Git](http://git-scm.com/)
* [Docker](https://www.docker.com/)
* [Oracle Autonomous Data Warehouse Instance](https://cloud.oracle.com/en_US/datawarehouse)

## Installation

* run `git clone https://github.com/caseyr003/adw-scale-python.git`

## Setup

Getting the Autonomous Data Warehouse Wallet files
* Navigate to your ADW instance on the Oracle Cloud Infrastructure Console
* Click 'DB Connection'
* Download the Client Credentials (Wallet)
* Unzip the files and place them in the `wallet` folder in this project

Updating Python app
* Update `app.py` with the ADW credentials
* Update `app.py` with OCI credential information

## Running

To run the project locally follow the following steps:

* change into the project directory
* `docker build -t python/adw-scale .`
* `docker run python/adw-scale`
or for development
* `docker run -v [LOCAL_PROJECT_PATH]:/app python/adw-scale`

## Demo
 
 After you start the docker container, the cpu usage of the ADW instance will be monitored and scaled using the OCI API. If you need workloads to run, you can find sample queries in the workloads.sql to run against the sample data provided in ADW. For the demo this is only configured to scale from 1 CPU to 2 because of environment constraints.
