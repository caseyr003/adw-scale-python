import json
import os
import time
import oci


class OCI_API:
    def __init__(self, tenancy_ocid, user_ocid, region, fingerprint, key_location):
        self.tenancy_ocid = tenancy_ocid
        self.user_ocid = user_ocid
        self.region = region
        self.fingerprint = fingerprint
        self.key_location = key_location
        self.config = "oci_config"
        self.config_account()

    def get_json(self):
        return {
            'tenancy_ocid': self.tenancy_ocid,
            'user_ocid': self.user_ocid,
            'region': self.region,
            'fingerprint': self.fingerprint,
            'key_location': self.key_location,
            'config_file': self.config
        }

    def config_account(self):
        config = open(self.config, 'w')
        config.seek(0)
        config.truncate()
        config.write('[DEFAULT]\n')
        config.write('user=%s\n' % self.user_ocid)
        config.write('fingerprint=%s\n' % self.fingerprint)
        config.write('key_file=%s\n' % self.key_location)
        config.write('tenancy=%s\n' % self.tenancy_ocid)
        config.write('region=%s\n' % self.region)
        config.close()

    def is_active(self):
        success = False
        try:
            config = oci.config.from_file(file_location=self.config)
            oci.identity.IdentityClient(config).get_user(config["user"])
            success = True
        except:
            print("An Error Occured")

        return success

    def list_adw_instances(self, compartment_id):
        try:
            config = oci.config.from_file(file_location=self.config)
            database = oci.database.DatabaseClient(config)
            adw = database.list_autonomous_data_warehouses(compartment_id)
            return adw
        except:
            print("An Error Occured")
            return "error"

    def get_adw(self, adw_ocid):
        try:
            config = oci.config.from_file(file_location=self.config)
            database = oci.database.DatabaseClient(config)
            adw = database.get_autonomous_data_warehouse(adw_ocid)
            return adw
        except:
            print("An Error Occured")
            return "error"

    def is_adw_available(self, adw_ocid):
        try:
            config = oci.config.from_file(file_location=self.config)
            database = oci.database.DatabaseClient(config)
            status = database.get_autonomous_data_warehouse(adw_ocid).data.lifecycle_state
            return status == "AVAILABLE"
        except:
            print("An Error Occured")
            return "error"

    def get_adw_cpu(self, adw_ocid):
        try:
            config = oci.config.from_file(file_location=self.config)
            database = oci.database.DatabaseClient(config)
            return database.get_autonomous_data_warehouse(adw_ocid).data.cpu_core_count
        except:
            print("An Error Occured")
            return "error"

    def scale_up_adw(self, adw_ocid):
        try:
            config = oci.config.from_file(file_location=self.config)
            database = oci.database.DatabaseClient(config)
            adw_details = oci.database.models.UpdateAutonomousDataWarehouseDetails(cpu_core_count=2)
            adw = database.update_autonomous_data_warehouse(adw_ocid, adw_details)
            return adw
        except:
            print("An Error Occured")
            return "error"
            
    def scale_down_adw(self, adw_ocid):
        try:
            config = oci.config.from_file(file_location=self.config)
            database = oci.database.DatabaseClient(config)
            adw_details = oci.database.models.UpdateAutonomousDataWarehouseDetails(cpu_core_count=1)
            adw = database.update_autonomous_data_warehouse(adw_ocid, adw_details)
            return adw
        except:
            print("An Error Occured")
            return "error"
