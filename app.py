import cx_Oracle
import time
from oci_api import OCI_API
import sys

# Update for accesss to the OCI API to scale ADW instance
TENANCY_OCID = "<tenancy_ocid>"
USER_OCID = "<user_ocid>"
REGION = "<us-phoenix-1>"
FINGERPRINT = "<user_fingerprint>"
KEY = "<location_api_key>"

# automonous data warehouse connection constants
# update below with your db credentials
# add wallet files to wallet folder
DB = "<database_connection_name_in_tnsnames.ora>"
DB_USER = "<database_user>"
DB_PASSWORD = "<database_password>"
ADW_OCID = "<adw_ocid>"

# Initialize connection to ADW database to query cpu usage
connection = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB)

# Initialize OCI API helper class
oci_api = OCI_API(TENANCY_OCID, USER_OCID, REGION, FINGERPRINT, KEY)

# Keep track of ocpu count and utilization
# Initialize utilization at 50% so no scaling occurs before query
scale_up_utilization = 60
scale_down_utilization = 30
ocpu_utilization = 50
cpu_count = 1
adw_available = True

def get_cpu_usage():
    cursor = connection.cursor()
    utilization = cursor.execute("select round(util/cpus*100) from (SELECT sum(AVG_CPU_UTILIZATION) util, max(cpu_utilization_limit) cpus from v$rsrcmgrmetric) u").fetchone()
    return utilization[0]

while True:
    if adw_available:
        ocpu_utilization = get_cpu_usage()
        adw_available = oci_api.is_adw_available(ADW_OCID)
        cpu_count = oci_api.is_adw_available(ADW_OCID)
        sys.stdout.write('\rCPU Utilization: ' + str(ocpu_utilization) + '%')
        sys.stdout.flush()
        if ocpu_utilization > 60 and cpu_count == 1:
            oci_api.scale_up_adw(ADW_OCID)
            sys.stdout.write('\rScaling Up to 2 CPUs')
            time.sleep(60)
        if ocpu_utilization < 30 and cpu_count == 2:
            oci_api.scale_down_adw(ADW_OCID)
            sys.stdout.write('\rScaling Down to 1 CPUs')
            time.sleep(60)
        time.sleep(1)
    else:
        adw_available = oci_api.is_adw_available(ADW_OCID)
        time.sleep(2)
