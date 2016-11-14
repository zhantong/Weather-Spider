import urllib.request
import json
import re


def get_city_list():
    url = 'http://www.nmc.cn/f/rest/autocomplete?q=&limit=10000'
    content = None
    with urllib.request.urlopen(url) as f:
        content = f.read().decode('utf-8')
    reg = re.compile(
        r'(?P<station_code>\d*)\|(?P<city>\w*)\|(?P<zip>\d*)\|(?P<province>\w*)\|(?P<pinyin>\w*)\|(?P<city_code>\w*)')
    result = [row.groupdict() for row in reg.finditer(content)]
    return result


def get_station_code(city, city_list):
    for row in city_list:
        if city == row['city']:
            return row['station_code']
    return None


def get_real_time_weather(station_code):
    url = 'http://www.nmc.cn/f/rest/real' + '/' + station_code
    content = None
    with urllib.request.urlopen(url) as f:
        content = f.read().decode('utf-8')
        content = json.loads(content)
    result = {
        'time': content['publish_time'],
        'city': content['station']['city'],
        'code': content['station']['code'],
        'temperature': content['weather']['temperature'],
        'rain': content['weather']['rain'],
        'info': content['weather']['info'],
        'feelst': content['weather']['feelst'],
        'humidity': content['weather']['humidity'],
        'rcomfort': content['weather']['rcomfort'],
        'airpressure': content['weather']['airpressure'],
        'wind_speed': content['wind']['speed'],
        'wind_power': content['wind']['power'],
        'wind_direct': content['wind']['direct']
    }
    return result

if __name__ == '__main__':
    station_code = get_station_code('北京', get_city_list())
    print(get_real_time_weather(station_code))
