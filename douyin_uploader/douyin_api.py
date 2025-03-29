import requests


def get_web_userinfo(unique_id) -> str:
    """
    根据抖音号获取用户信息
    :param unique_id:
    :return:
    """
    url = "https://www.iesdouyin.com/web/api/v2/user/info/?unique_id={}".format(unique_id)
    res = requests.get(url, headers={"User-Agent": self.ua["web"]}).json()
    n = 0
    while True:
        n += 1
        try:
            nickname = res["user_info"]["nickname"]
            break
        except KeyError:
            print("获取用户昵称失败！")
        if n > 3:
            nickname = ''
            break
    return nickname


