import csv
import os

# NOTE: NEED TO CHANGE {username} to "mycarbonenactus" if testing on enactus' site, vice versa
# PROJECT_HOME = '/home/weiernt/enactus-site'
PROJECT_HOME = '/home/mycarbonenactus/enactus-site'

def check_csv(csv_file=PROJECT_HOME+"/csv_stuff/csv_file.csv"):
    """Does the csv_data file exist? if yes, then return true, oterwise false"""
    return os.path.isfile(csv_file)

# INIT csv using dictreader for fieldnames
def init_csv():
    """initliaises a new csv to be used. NOTE THIS DESTROYS the old data csv"""
    with open(PROJECT_HOME + "/csv_stuff/csv_file.csv", "w", newline="") as f:
        fieldnames = ["first_name", "last_name", "email", "price_created", "carbon_emit_tonnes_per_month", "plan_id", "percentage_offset"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    return


def add_row(first_name, last_name, email, price_created, carbon_emit_tonnes_per_month, plan_id, percentage_offset):
    """Adds a data entry into the csv, is done """
    fieldnames = ["first_name", "last_name", "email", "price_created", "carbon_emit_tonnes_per_month", "plan_id", "percentage_offset"]

    with open(PROJECT_HOME + "/csv_stuff/csv_file.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow({"first_name": first_name, "last_name": last_name, "email": email, 
                            "price_created": price_created, 
                            "carbon_emit_tonnes_per_month": carbon_emit_tonnes_per_month, 
                            "plan_id": plan_id,
                            "percentage_offset": percentage_offset})



def read_csv():
    """"Just for testing, reads the csv file containing the user data"""
    with open(PROJECT_HOME + "/csv_stuff/csv_file.csv", "r", newline="") as f:
        r = csv.reader(f)
        for i in r:
            print(i)

    