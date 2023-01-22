import glob
import os
import pandas
from flask import Flask
from flask_caching import Cache
from config import *

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)

def load_latest_file(glob_path):
    latest_file = None
    list_of_files = glob.glob(glob_path) # * means all if need specific format then *.csv
    try:
        latest_file = max(list_of_files, key=os.path.getctime)
    except ValueError:
        pass
    return latest_file

def load_config_file(glob_file_path):
    return load_latest_file(f"{CONFIG_PATH}{os.sep}{glob_file_path}")

def load_eventdata_file(glob_file_path):
    return load_latest_file(f"{EVENTDATA_PATH}{os.sep}{glob_file_path}")

def read_csv_to_dict(file_path):
    return pandas.read_csv(file_path, keep_default_na=False).to_dict(orient="records")

def normalize_keys(data):
    normalized_data = {}
    for key in data:
        normalized_key = key.lower()
        normalized_key = normalized_key.replace(" ", "_")
        normalized_data[normalized_key] = data[key]
    return normalized_data

def csv_data_to_json_response(file_path, sort_function=None, success_message = "data file loaded", file_not_found_message="data file could not be found", file_corrupt_message="data file is corrupt or not in the correct format"):
    response = {}

    data = []
    if file_path:
        try:
            data = read_csv_to_dict(file_path)

            if sort_function is not None:
                data.sort(key=sort_function)

            data = [normalize_keys(item) for item in data]

            response['status'] = "success"
            response['data'] = data
            response['message'] = success_message
        except (ValueError, KeyError):
            response['status'] = "error"
            response['data'] = data
            response['message'] = file_corrupt_message
    else:
        response['status'] = "error"
        response['data'] = data
        response['message'] = file_not_found_message

    return response

@app.route("/")
def root():
    return "<p>This is MJAPI. An API service used in conjunction with M&J Timing.</p>"


@app.route("/api/config")
def config():
    config_data_file_path = load_config_file("configData.csv")
    return csv_data_to_json_response(config_data_file_path,
            success_message="config data loaded.",
            file_corrupt_message="config data is corrupted or not in the correct format.",
            file_not_found_message="could not find config data. Check '" + CONFIG_PATH + "' for config data information."
            )

@app.route("/api/classes")
def classes():
    class_data_file_path = load_config_file("*classData.csv")
    
    return csv_data_to_json_response(class_data_file_path,
            sort_function=lambda class_type: class_type['Display Order'],
            success_message="class data loaded.",
            file_corrupt_message="class data is corrupted or not in the correct format.",
            file_not_found_message="could not find class data. check '" + CONFIG_PATH + "' for class data information."
            )

@app.route("/api/drivers")
def drivers():
    driver_data_file_path = load_eventdata_file("*driverData.csv")
    
    return csv_data_to_json_response(driver_data_file_path,
            success_message="driver data loaded.",
            file_corrupt_message="driver data is corrupted or not in the correct format.",
            file_not_found_message="could not find driver data. Check '" + EVENTDATA_PATH + "' for driver data information."
            )

@app.route("/api/runs")
@cache.cached(timeout=2)
def runs():
    timing_data_file_path = load_eventdata_file("*timingData.csv")
    
    return csv_data_to_json_response(timing_data_file_path,
            sort_function=lambda run: run["run_number"],
            success_message="timing data loaded.",
            file_corrupt_message="timing data is corrupted or not in the correct format.",
            file_not_found_message="could not find timing data. Check '" + EVENTDATA_PATH + "' for timing data information."
            )
