import json 

class WeatherDataParser():
    def __init__(self):
        print("WeatherDataParser intiallized")

    def parse_temperature_sensor_json(self, input_json, target_key, target_date):
        if type(input_json) is dict and input_json:
            matching = []
            for key in input_json:
                if key == target_key and target_date in input_json[key]:
                    return {'DATETIME':input_json[key], 'AT':input_json['AT']}
                res = self.parse_temperature_sensor_json(input_json[key], target_key, target_date)
                if res:
                    matching.append(res)
            if len(matching) > 0:
                return matching
            else:
                return False
        elif type(input_json) is list and input_json:
            matching = []
            for entity in input_json:
                res = self.parse_temperature_sensor_json(entity, target_key, target_date)
                if res:
                    matching.append(res)
            if len(matching) > 0:
                return matching
            else:
                return False

    def parse_wind_sensor_json(self, input_json, target_key, target_date):
        if type(input_json) is dict and input_json:
            matching = []
            for key in input_json:
                if key == target_key and target_date in input_json[key]:
                    return {'DATETIME':input_json[key], 'WD':input_json['WD']}
                res = self.parse_wind_sensor_json(input_json[key], target_key, target_date)
                if res:
                    matching.append(res)
            if len(matching) > 0:
                return matching
            else:
                return False
        elif type(input_json) is list and input_json:
            matching = []
            for entity in input_json:
                res = self.parse_wind_sensor_json(entity, target_key, target_date)
                if res:
                    matching.append(res)
            if len(matching) > 0:
                return matching
            else:
                return False

    def parseLog4Weather(self, date):
        with open("./logs/currentSensorData.json",'r') as fp:
            data = json.loads(fp.read())
            fp.close()
        First_UTCResultT = self.parse_temperature_sensor_json(data,'First_UTC',date)
        Last_UTCResultT = self.parse_temperature_sensor_json(data,'Last_UTC',date)
        First_UTCResultW = self.parse_wind_sensor_json(data,'First_UTC',date)
        Last_UTCResultW = self.parse_wind_sensor_json(data,'Last_UTC',date)
        resultTemp = First_UTCResultT if First_UTCResultT else Last_UTCResultT
        resultWind = First_UTCResultW if First_UTCResultW else Last_UTCResultW
        return {'Temperature':resultTemp, 'Wind':resultWind}
