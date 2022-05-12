from typing import List
from .hex_to_data import decoder
import logging
import json
import azure.functions as func


def main(events: List[func.EventHubEvent]):
    for event in events:
        # logging.info('Python EventHub trigger processed an event: %s',
        #                 event.get_body().decode('utf-8'))

        data = event.get_body().decode('utf-8')
        json_data = json.loads(data)

        cmd = json_data['cmd']

        if (cmd == 'rx'):
            sensor_eui = json_data['EUI']
            count = json_data['fcnt']
            sensor_data = json_data['data']
            temperature = decoder(sensor_data)["temperature"]
            humidity = decoder(sensor_data)["humidity"]

            logging.info('Sensor ID: ' + sensor_eui)
            logging.info('Uplink Count: ' + str(count))
            logging.info('Data: ' + sensor_data)
            logging.info('Temperature: ' + str(temperature))
            logging.info('Humidity: ' + str(humidity))

            