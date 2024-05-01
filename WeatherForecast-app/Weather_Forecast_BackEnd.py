import requests
from flask import Response
import boto3
import json
import os


def convert_to_geolocation(location):
    result = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json").json()
    latitude = longitude = name = country = None
    if 'results' not in result.keys():
        return latitude, longitude, name, country
    latitude = result['results'][0]['latitude']
    longitude = result['results'][0]['longitude']
    name = result['results'][0]['name']
    country = result['results'][0]['country']
    return latitude, longitude, name, country


def get_forecast(latitude, longitude):
    result = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,"
        f"temperature_2m_min,relative_humidity_2m_mean").json()

    return result


def parse_data(data):
    seven_day_data = {}

    for i in range(len(data['daily']['time'])):
        seven_day_data[i + 1] = []
        seven_day_data[i + 1].append(data['daily']['time'][i])
        seven_day_data[i + 1].append(data['daily']['temperature_2m_max'][i])
        seven_day_data[i + 1].append(data['daily']['temperature_2m_min'][i])
        seven_day_data[i + 1].append(data['daily']['relative_humidity_2m_mean'][i])

    return seven_day_data


def convert_location_to_forecast(user_location):
    user_location_latitude, user_location_longitude, user_location_name, user_location_country \
        = convert_to_geolocation(user_location)
    if user_location_name is None:
        return None, None, None

    location_data = get_forecast(user_location_latitude, user_location_longitude)
    return parse_data(location_data), user_location_name, user_location_country


def download_image():
    s3_client = boto3.client('s3')
    obj = s3_client.get_object(Bucket="waitzman.com", Key="sky.jpeg")
    return Response(obj["Body"].read(), mimetype='Content-Type',
                    headers={'Content-Disposition': 'attachment; filename=sky.jpeg'})


def dynamodb_send_item(items, location_name):
    dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

    def convert_to_dynamodb_type(value):
        if isinstance(value, list):
            return {'L': [convert_to_dynamodb_type(item) for item in value]}
        elif isinstance(value, int):
            return {'N': str(value)}
        elif isinstance(value, float):
            return {'N': str(value)}
        elif isinstance(value, bool):
            return {'BOOL': value}
        else:
            return {'S': str(value)}
    dyn_items = []
    for key, value in items.items():
        dyn_items.append(convert_to_dynamodb_type(value))

    response = dynamodb.put_item(
        TableName="WeatherForecast",
        Item={
            "data": {"S": str(f"{location_name} {items[1][0]}")},
            "weather": {"L": dyn_items}
        }
    )
    # response = None
    return response

def save_history(data, location_name, location_country):
    file_name = f"{location_name}-{location_country}-{data[1][0]}"
    json_object = json.dumps(data, indent=7)
    with open(f"history/{file_name}.json", "w") as outfile:
        outfile.write(json_object)

def get_history_files():
    directory = 'history'
    history_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return history_files

if __name__ == "__main__":
    data, location_name, location_country = convert_location_to_forecast("bat yam")
    print(data, location_name, location_country)
    save_history(data, location_name, location_country)
