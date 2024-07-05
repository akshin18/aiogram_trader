import requests
import time

def recaptcha_solve(captcha_token, site_key):
                
        data = {
            "key":captcha_token,
            "method":"userrecaptcha",
            "googlekey":site_key,
            "pageurl":"https://fbsbx.com/captcha/recaptcha/iframe/",
            "json":1,
            "invisible":1
        }
        print(data)
        r = requests.post("http://rucaptcha.com/in.php",data=data)
        resp = r.json()
        print(resp)
        if resp["status"] == 1:
            id_ = resp["request"]
            params = {
                "key":captcha_token,
                "action":"get",
                "id":id_,
                "json":1
            }
            while True:
                r = requests.get("http://rucaptcha.com/res.php",params=params)
                resp = r.json()
                print(r.status_code,resp)
                if resp["status"] == 1:
                    return resp["request"]

                time.sleep(2)
                

recaptcha_solve(
    "867b7a399a80ced7eb554bd16b3c9713",
    # "6Lc9qjcUAAAAADTnJq5kJMjN9aD1lxpRLMnCS2TR"
    #  "6LfD3PIbAAAAAJs_eEHvoOl75_83eXSqpPSRFJ_u"
    "6LdktRgnAAAAAFQ6icovYI2-masYLFjEFyzQzpix"
)