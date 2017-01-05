import urllib.request
import json
import re
import base64
from datetime import datetime

POLLUTANT = {
    '1': 'PM10',
    '2': 'SO2',
    '3': 'PM2.5',
    '4': 'O3',
    '5': 'NO2',
    '6': 'CO'
}


def get_real_time_environment():
    url = 'http://zx.bjmemc.com.cn/index.shtml'
    content = None
    with urllib.request.urlopen(url) as f:
        content = f.read().decode('utf-8')
    now_data_var_name = re.findall(r'var\snowdata.*?\+(.*?)\+', content)[0]
    content_base64_encode = re.findall(
        r'var\s%s.*?decode\((.*?)\)' % now_data_var_name, content)[0]
    content = base64.b64decode(content_base64_encode).decode('utf-8')
    content = json.loads(content)

    time = str(datetime.utcfromtimestamp(int(content['date_f'])))
    priority_pollutant = POLLUTANT[content['first']]
    station = '北京市'

    so2 = content.get('so2')
    so2_iaqi = content.get('so2_01')
    so2_level = content.get('so2_02')

    pm10 = content.get('pm10')
    pm10_iaqi = content.get('pm10_01')
    pm10_level = content.get('pm10_02')

    pm2 = content.get('pm2')
    pm2_iaqi = content.get('pm2_01')
    pm2_level = content.get('pm2_02')

    no2 = content.get('no2')
    no2_iaqi = content.get('no2_01')
    no2_level = content.get('no2_02')

    o3 = content.get('o3')
    o3_iaqi = content.get('o3_01')
    o3_level = content.get('o3_02')

    co = content.get('co')
    co_iaqi = content.get('co_01')
    co_level = content.get('co_02')

    result = {
        'time': time,
        'station': station,
        'priority_pollutant': priority_pollutant,
        'pollutants': [
            {
                'pollutant': 'SO2',
                'value': so2,
                'iaqi': so2_iaqi,
                'qlevel': so2_level
            },
            {
                'pollutant': 'PM10',
                'value': pm10,
                'iaqi': pm10_iaqi,
                'qlevel': pm10_level
            },
            {
                'pollutant': 'PM2.5',
                'value': pm2,
                'iaqi': pm2_iaqi,
                'qlevel': pm2_level
            },
            {
                'pollutant': 'NO2',
                'value': no2,
                'iaqi': no2_iaqi,
                'qlevel': no2_level
            },
            {
                'pollutant': 'O3',
                'value': o3,
                'iaqi': o3_iaqi,
                'qlevel': o3_level
            },
            {
                'pollutant': 'CO',
                'value': co,
                'iaqi': co_iaqi,
                'qlevel': co_level
            }
        ]
    }
    return result

if __name__ == '__main__':
    result = get_real_time_environment()
    print(result)
