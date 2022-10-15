import requests
import re 

class TelegramApi:
    def __init__(self, phone_number):
        session = requests.Session()
        
        req = session.post("https://my.telegram.org/auth/send_password", data={"phone": phone_number})
        random_hash = req.json()["random_hash"]

        self.random_hash = random_hash
        self.phone_number = phone_number
        self.session = session

    def enter_code(self, code):
        req = self.session.post("https://my.telegram.org/auth/login", data={"phone": self.phone_number, "random_hash": self.random_hash, "password": code})

        if req.status_code != 200:
            raise Exception("Invalid code")
        return True

    def create_app(self):
        appData = self._check_appData()
        if appData != None:
            self.app = appData
            return
        
        hash_main = self.check_hash()
        self._create_app(hash_main)

        self.app = self._check_appData()
        return

    def _create_app(self, hash):
        req = self.session.post("https://my.telegram.org/apps/create", data={"hash": hash, "app_desc": "fsiafhiwahifhaw", "app_shortname": "dfsadkfdskf", "app_title": "dskafddfsakdfs", "app_platform": "android", "app_url": ""})
        return req

    def _check_hash(self):
        req = self.session.get("https://my.telegram.org/apps")
        content = req.content.decode('utf-8')

        return self._search_hash(content)


    def _check_appData(self):
        req_e = self.session.get("https://my.telegram.org/apps")
        content = req_e.content.decode('utf-8')

        return self._search_appData(content)

    def _search_hash(self, content):
        hash_input = re.findall(r'<input type="hidden" name="hash" value="\S+"\/>', content)
        if len(hash_input) == 0:
            return None
        hash_input = hash_input[0]
        hash_value = re.findall(r'value="\S+"', hash_input)[0]
        hash_main = hash_value.replace("value=", "").replace("\"", "").replace("\"", "")

        return hash_main

    def _search_appData(self, content):
        data_input = re.findall(r'<span class="form-control input-xlarge uneditable-input" onclick="this.select\(\);">\S+<\/span>', content)

        if len(data_input) == 0:
            return None

        api_id = data_input[0].replace('<span class="form-control input-xlarge uneditable-input" onclick="this.select();">', '').replace('</span>', '').replace("<strong>", "").replace("</strong>", "")
        api_hash = data_input[1].replace('<span class="form-control input-xlarge uneditable-input" onclick="this.select();">', '').replace('</span>', '')

        return (api_id, api_hash)

account = ApiData(number)
account.enter_code(input())
account.create_app()

print(account.app)