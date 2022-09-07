import requests
import json
from datetime import datetime
import re


class Test_1():
    url_part1 = 'https://api.chucknorris.io/jokes/'
    url_part2 = 'random'
    # why do you need 2 parts?
    api_url = url_part1 + url_part2

    def send_request(self):
        r = requests.get(url = self.api_url)
        if r.status_code != 200:
            print("\nwrong status code received :", r.status_code)
            return None
        else:
            return r.text

    def test_1_good_path(self):
        print("\n***** Running GOOD PATH test")
        text = self.send_request()
        if text :
             print("\n GOOD PATH test passed !")

    def test_2_check_response_fields(self):
        print("\n***** Running response_fields test")
        test_result= False
        text = self.send_request()
        if text :
            json_text = json.loads(text)
            print("\nChecking fields , request output:", json_text)           
            categories = json_text["categories"]
            created_at = json_text["created_at"]
            icon_url = json_text["icon_url"]
            id = json_text["id"]
            updated_at = json_text["updated_at"]
            url = json_text["url"]
            value = json_text["value"]

            if not value :
                print("\nTest failed , value field should not be empty")
            else:
                #why defining a new function if you could test it in line 36
                test_result = self.verify_icon_url(icon_url)
                if test_result is True:
                    test_result = self.verify_id_and_url(id,url)
                if test_result is True:
                    test_result = self.verify_created_and_updated_dates(created_at, updated_at)
                if test_result is False:
                    print("\nTest failed")


    def verify_icon_url(self, icon_url):
        if not icon_url:
            print("\nTest failed , icon_url field should not be empty", icon_url)
            return False
        else:
            if icon_url != 'https://assets.chucknorris.host/img/avatar/chuck-norris.png':
                print("\nTest failed , icon_url field content is incorrect: ", icon_url)
                return False
        print("\n icon_url is OK")
        return True


    def verify_id_and_url(self, id,url):
        if len(id) != 22:
            print("\nTest failed , id field length is incorrect: ", len(id))
            return False
        else:
            valid = re.match("^[A-Za-z0-9_-]*$", id)
            if not valid:
                print("\nTest failed , id contains invalid characters : ", id)
                return False
            else:
                part1, part2 =url.split(self.url_part1)
                if part2:
                    if part2 != id:
                        print("\nTest failed , id in url should be the same as id content  : ", part2)
                        return False
                else:
                    print("\nTest failed , id in url is wrong  : ", part2)
                    return False
        print("\n id_and_url are OK ")
        return True

    def verify_created_and_updated_dates(self,created_at, updated_at):
        if not created_at :
            print("\nTest failed , created _at field is empty : ")
            return False
        else:
            if not updated_at:
                print("\nTest failed , updated_at field is empty : ")
                return False
        try:
            created = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f")
        except:
            print("\nTest failed , incorrect created_at field format ")
            return False

        try:
            updated = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S.%f")
        except:
            print("\nTest failed , incorrect updated_at field format ")
            return False

        if updated < created:
            print("\nTest failed , updated_at field must be later than created_at: ")
            return False
        print("\n created_at, updated_at are OK ")
        return True

    def test_3_different_value_for_different_ids(self):
        print("\n***** Running different_value_for_different_ids test")
        id1 = None
        id2 = None
        value1 = None
        value2 = None

        text = self.send_request()
        if text :
            json_text = json.loads(text)
            # you are using id1 in this function, while you used id variable for the same purpose in another function.
            id1 = json_text["id"]
            value1 = json_text["value"]

        text = self.send_request()
        if text :
            json_text = json.loads(text)
            id2 = json_text["id"]
            value2 = json_text["value"]

        if id1 != id2 :
            if value1 == value2:
                print("\nTest failed , value content should be different for different ids ")
            else:
                print("\n different_value_for_different_ids is OK ")




