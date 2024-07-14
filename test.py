# import requests

# header = {"User-Agent": "Instagram 219.0.0.12.117 Android", "x-ig-app-id":"936619743392459"}
# username = "qew3f43frew"
# response = requests.get(f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}", headers=header)
# if response.status_code in [200, 201]:
#     with open("a.txt", "w") as f:
#         f.write(response.text)
#     # user actually exists
#     # print(response.text)
# else:
#     print(response.status_code)
#     print(response.text)


# import requests

# header = {"User-Agent": "Instagram 219.0.0.12.117 Android", "x-ig-app-id":"936619743392459"}
# username = "leomessi"
# response = requests.get(f"https://www.instagram.com/api/v1/feed/user/{username}/username/", headers=header)
# if response.status_code in [200, 201]:
#     with open("a.txt", "w") as f:
#         f.write(response.text)
#     # user actually exists
#     # print(response.text)
# else:
#     print(response.status_code)
#     print(response.text)

########################################################
# import requests

# url = "https://www.instagram.com/p/C9K1-VAAenz/?__a=1&__d=dis"

# payload = {}
# headers = {
#     "User-Agent": "Instagram 279.0.0.12.117 Android", "x-ig-app-id":"936619743392459",
#   'x-instagram-gis': '00a89418c3a4f92d5407e36116117cd9',
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# with open("a.txt", "w") as f:
#     f.write(response.text)

########################################################
# import json
# from typing import Dict
# from urllib.parse import quote

# import requests

# INSTAGRAM_APP_ID = "936619743392459"  # this is the public app id for instagram.com


# def scrape_post(url_or_shortcode: str) -> Dict:
#     """Scrape single Instagram post data"""
#     if "http" in url_or_shortcode:
#         shortcode = url_or_shortcode.split("/p/")[-1].split("/")[0]
#     else:
#         shortcode = url_or_shortcode
#     print(f"scraping instagram post: {shortcode}")

#     variables = {
#         "shortcode": shortcode,
#         "child_comment_count": 20,
#         "fetch_comment_count": 100,
#         "parent_comment_count": 24,
#         "has_threaded_comments": True,
#     }
#     url = "https://www.instagram.com/graphql/query/?query_hash=b3055c01b4b222b8a47dc12b090e4e64&variables="
#     result = requests.get(
#         url=url + quote(json.dumps(variables)),
#         headers={"x-ig-app-id": INSTAGRAM_APP_ID},
#     )
#     data = json.loads(result.content)
#     # return data["data"]["shortcode_media"]
#     return result.text

# # Example usage:
# posts = scrape_post("https://www.instagram.com/p/C9K1-VAAenz/")
# # print(json.dumps(posts, indent=2, ensure_ascii=False))

# with open("a.txt", "w") as f:
#     f.write(posts)

#######################################################


# import json
# import requests
# from urllib.parse import quote

# def scrape_user_posts(user_id: str, session: requests.Session, page_size=12, max_pages: int = None):
#     base_url = "https://www.instagram.com/graphql/query/?query_hash=56a7068fea504063273cc2120ffd54f3&variables="
#     variables = {
#         "id": user_id,
#         "first": page_size,
#         "after": None,
#         # "include_reel": True,
#         # "fetch_mutual": True,
#         # "tag_name": "yolcuyevhh_"
#     }
#     _page_number = 1
#     p = "http://brd-customer-hl_e7f8a697-zone-scraping_proxies_2-ip-168.151.134.43:pzcv3bh3wszw@brd.superproxy.io:22225"
#     proxies = {
#         "https":p,
#         "http": p
#     }
#     cookies = {
#         "sessionid":"67261654726%3AkNAIL0rAJ5JLhH%3A18%3AAYdLY1crdGGbN4Mf7FBY0ymi4jksvszdKNXV6zFxrg"
#     }
#     while True:
#         url = base_url + quote(json.dumps(variables))

#         resp = session.get(url, proxies=proxies,cookies=cookies)
#         data = resp.json()
#         with open("a.txt", "w") as f:
#             f.write(resp.text)
#         break
#         posts = data["data"]["user"]["edge_owner_to_timeline_media"]
#         for post in posts["edges"]:
#             yield post["node"]
#         page_info = posts["page_info"]
#         if _page_number == 1:
#             print(f"scraping total {posts['count']} posts of {user_id}")
#         else:
#             print(f"scraping page {_page_number}")
#         if not page_info["has_next_page"]:
#             break
#         if variables["after"] == page_info["end_cursor"]:
#             break
#         variables["after"] = page_info["end_cursor"]
#         _page_number += 1
#         if max_pages and _page_number > max_pages:
#             break


# # Example run:
# if __name__ == "__main__":
#     with requests.Session() as session:
#         posts = list(scrape_user_posts("3510714521", session, max_pages=3))
#         # print(json.dumps(posts, indent=2, ensure_ascii=False))
#         # with open("a.txt", "w") as f:
#         #     f.write(json.dumps(posts, indent=2, ensure_ascii=False))


#######################################################
# import requests

# r = requests.get("https://instagram.com/graphql/query/?query_id=17888483320059182&id=1067259270&first=240")
# with open("a.txt", "w") as f:
#     f.write(r.text)

# from urllib.parse import quote
# import requests
# import json

# variables = {
#     "data": {
#         "device_id": "38680F99-6C7B-46F0-8F75-0AB8E995F763",
#         "is_async_ads_double_request": "0",
#         "is_async_ads_in_headload_enabled": "0",
#         "is_async_ads_rti": "0",
#         "rti_delivery_backend": "0",
#         "feed_view_info": '[{"media_id":"3409241445668971550_5677458825","media_pct":1,"time_info":{"10":121541,"25":121541,"50":121541,"75":121541},"version":24}]',
#     },
#     "variant": "home",
#     "__relay_internal__pv__PolarisFeedShareMenurelayprovider": True,
# }

# headers = {
#     "Cookies":'mid=ZiF2eAAEAAFlHJFYjIUi4gZkxOvF; ig_did=38680F99-6C7B-46F0-8F75-0AB8E995F763; datr=eHYhZtdzCBftzoiuFu4tYEcN; ig_nrcb=1; oo=v1; ps_n=1; ps_l=1; ds_user_id=6417125073; shbid="19425\0546417125073\0541752056567:01f7295744d765b5362aa0989ed03659bdddc427161406164dac7f206fff0ee72ec1e26e"; shbts="1720520567\0546417125073\0541752056567:01f731fd24903bef61739feb381f1438f15db0167c827a826b95fb0e2af0187210542c5f"; csrftoken=8t4X1CxDdex3qAyklQx3IwRwuoxlBfHO; wd=1492x924; sessionid=6417125073%3AMiTAX3mJmmlwLD%3A9%3AAYdcDrg-fD4fpY33TKmzVW4LAdMSqIhd_Th0tBo-t0c; rur="VLL\0546417125073\0541752244649:01f7b5754cc0222744b7ae59f664c68e1327a1955c54b0d9e4b6b4c37ebe3cfdd92232f8"'
# }
# r = requests.get(
#     "https://instagram.com/graphql/query/?query_id=7495510263850612&variables="
#     + quote(json.dumps(variables)),
#     headers=headers,
# )
# with open("a.txt", "w") as f:
#     f.write(r.text)

