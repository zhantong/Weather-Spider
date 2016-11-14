import urllib.request
import json


def get_real_time_environment():
    url = 'http://zx.bjmemc.com.cn/web/Service.ashx'
    content = None
    with urllib.request.urlopen(url) as f:
        content = f.read().decode('utf-8')
        content = json.loads(content)
    result = {
        'time': content['Table'][0]['Date_Time'],
        'station': content['Table'][0]['station'],
        'priority_pollutant': content['Table'][0]['PriPollutant'],
        'pollutants': []
    }
    for row in content['Table']:
        result['pollutants'].append({
            'pollutant': row['Pollutant'],
            'value': row['Value'],
            'iaqi': row['IAQI'],
            'qlevel': row['QLevel'],
            'quality': row['Quality']
        })
    return result

if __name__ == '__main__':
    result = get_real_time_environment()
    print(result)
