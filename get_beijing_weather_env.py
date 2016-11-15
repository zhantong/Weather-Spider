import json
import pymysql
import get_weather
import get_environment
import logging
from email.mime.text import MIMEText
import smtplib

logging.basicConfig(filename='weather_env.log', level=logging.INFO)

DATABASE = 'beijing_weather'


class Beijing():

    def __init__(self):
        self.db = None
        self.db = self.db_connect(DATABASE)

    def __del__(self):
        self.db_disconnect()

    def init_db(self):
        sql_create_weather_table = '''CREATE TABLE IF NOT EXISTS
            `weather`
            (
            `time` DATETIME NOT NULL,
            `city` VARCHAR(10) NOT NULL,
            `code` VARCHAR(10) NOT NULL,
            `temperature` VARCHAR(10) NOT NULL,
            `rain` VARCHAR(10) NOT NULL,
            `info` VARCHAR(20) NOT NULL,
            `feelst` VARCHAR(10) NOT NULL,
            `humidity` VARCHAR(10) NOT NULL,
            `rcomfort` VARCHAR(10) NOT NULL,
            `airpressure` VARCHAR(10) NOT NULL,
            `wind_speed` VARCHAR(10) NOT NULL,
            `wind_power` VARCHAR(10) NOT NULL,
            `wind_direct` VARCHAR(10) NOT NULL,
            PRIMARY KEY (`time`, `city`)
            )
            '''
        sql_create_environment_table = '''CREATE TABLE IF NOT EXISTS
            `environment`
            (
            `time` DATETIME NOT NULL,
            `station` VARCHAR(10) NOT NULL,
            `priority_pollutant` VARCHAR(10) NOT NULL,
            `pollutant` VARCHAR(10) NOT NULL,
            `value` VARCHAR(10) NOT NULL,
            `iaqi` VARCHAR(10) NOT NULL,
            `qlevel` VARCHAR(10) NOT NULL,
            `quality`  VARCHAR(10) NOT NULL,
            PRIMARY KEY (`time`, `station`, `pollutant`)
            )
            '''
        with self.db.cursor() as cursor:
            cursor.execute(sql_create_weather_table)
            cursor.fetchall()
            cursor.execute(sql_create_environment_table)
            cursor.fetchall()
        self.db.commit()

    def update_weather(self):
        weather = get_weather.get_real_time_weather(
            get_weather.get_station_code('北京', get_weather.get_city_list()))
        logging.info(json.dumps(weather))
        sql = '''INSERT IGNORE INTO `weather`
            (
            `time`,`city`,`code`,`temperature`,`rain`,`info`,`feelst`,
            `humidity`,`rcomfort`,`airpressure`,`wind_speed`,
            `wind_power`,`wind_direct`
            )
            VALUES
            (
            %(time)s,%(city)s,%(code)s,%(temperature)s,%(rain)s,%(info)s,
            %(feelst)s,%(humidity)s,%(rcomfort)s,%(airpressure)s,
            %(wind_speed)s,%(wind_power)s,%(wind_direct)s
            )'''
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql, weather)
        except Exception as e:
            send_mail('天气抓取出错', str(e), 'zhantong1994@163.com')
        self.db.commit()

    def update_environment(self):
        environment = get_environment.get_real_time_environment()
        logging.info(json.dumps(environment))
        sql = '''INSERT IGNORE INTO `environment`
            (
            `time`,`station`,`priority_pollutant`,`pollutant`,
            `value`,`iaqi`,`qlevel`,`quality`
            )
            VALUES
            (
            %s,%s,%s,%s,%s,%s,%s,%s
            )'''
        try:
            with self.db.cursor() as cursor:
                for item in environment['pollutants']:
                    cursor.execute(sql, (environment['time'], environment['station'], environment['priority_pollutant'], item['pollutant'], item[
                                   'value'], item['iaqi'], item['qlevel'], item['quality']))
        except Exception as e:
            send_mail('天气抓取出错', str(e), 'zhantong1994@163.com')
        self.db.commit()

    def db_connect(self, database):
        user, password = None, None
        with open('db_user_password.json', 'r', encoding='utf-8') as f:
            content = json.loads(f.read())
            user, password = content['user'], content['password']
        db = pymysql.connect(host='localhost',
                             user=user,
                             password=password,
                             db=database,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        return db

    def db_commit(self):
        if not self.db is None:
            self.db.commit()

    def db_disconnect(self):
        if not self.db is None:
            self.db.close()


def send_mail(subject, text, send_to):
    account_password_file = 'email_account_password.json'
    account, password = None, None
    with open(account_password_file, 'r', encoding='utf-8') as f:
        content = json.loads(f.read())
        account, password = content['account'], content['password']
        msg = MIMEText(text)
        msg['Subject'] = subject
        msg['From'] = account
        msg['To'] = send_to
        s = smtplib.SMTP(host='smtp.163.com')
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(account, password)
        s.send_message(msg)
        s.quit()
if __name__ == '__main__':
    beijing = Beijing()
    beijing.init_db()
    beijing.update_weather()
    beijing.update_environment()
