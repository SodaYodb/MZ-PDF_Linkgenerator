import requests
import json
import urllib.parse
from datetime import datetime

user_data = [
    # ID, Mail , password
    ['ID', 'MAIL', 'PASSWD'] # insert legit userdata here
]

login_url = "https://epaper.mz.de/delivery/v3/entitlement/login"
gen_info_url = "https://epaper.mz.de/"
graphql_addr = "https://epaper.mz.de/delivery/graphql"

addresses= [
    ["Ascherslebener Zeitung", "https://kiosk.purplemanager.com/mz-aschersleben#/main/issues", 1],
    ["Bernburger Kurier", "https://kiosk.purplemanager.com/mz-bernburger#/main/issues", 2],
    ["Bitterfelder Zeitung", "https://kiosk.purplemanager.com/mz-bitterfelder#/main/issues", 3],
    ["Anhalt-Kurier Dessau", "https://kiosk.purplemanager.com/mz-dessau#/main/issues", 4],
    ["Mansfelder Zeitung Eisleben", "https://kiosk.purplemanager.com/mz-eisleben#/main/issues", 5],
    ["Saalekurier Halle", "https://kiosk.purplemanager.com/mz-halle#/main/issues", 6],
    ["Mansfelder Zeitung Hettstedt", "https://kiosk.purplemanager.com/mz-hettstedt#/main/issues", 7],
    ["Elbe-Kurier Jessen", "https://kiosk.purplemanager.com/mz-jessen#/main/issues", 8],
    ["Köthener Zeitung", "https://kiosk.purplemanager.com/mz-koethener#/main/issues", 9],
    ["Neuer Landbote Merseburg", "https://kiosk.purplemanager.com/mz-merseburg#/main/issues", 10],
    ["Naumburger Tageblatt", "https://kiosk.purplemanager.com/mz-naumburger#/main/issues", 11],
    ["Naumburger Tageblatt Nebra", "https://kiosk.purplemanager.com/mz-nebra#/main/issues", 12],
    ["Quedlinburger Harzbote", "https://kiosk.purplemanager.com/mz-quedlinburger#/main/issues", 13],
    ["Sangerhäuser Zeitung", "https://kiosk.purplemanager.com/mz-sangerhaeuser#/main/issues", 14],
    ["Elbe-Kurier Wittenberg", "https://kiosk.purplemanager.com/mz-wittenberg#/main/issues", 15],
    ["Weißenfelser Zeitung", "https://kiosk.purplemanager.com/mz-weissenfelser#/main/issues", 16],
    ["Zeitzer Zeitung", "https://kiosk.purplemanager.com/mz-zeitzer#/main/issues", 17]
]

man_headers ={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers"
}

json_headers ={
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "DNT": "1",
    "Connection": "keep-alive",
    "content-type": "application/json",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
}

def perform_login(app_id, mail, password, man_headers):
    login_form_data = {
        'appId':app_id,
        'deviceId':'web',
        'preview':'false',
        'username':mail,
        'password':password}
    resp_login = requests.post(login_url, headers = man_headers, data=login_form_data)
    login_resp = resp_login.json()
    return login_resp['accessToken']
    
def get_doc_id(doc_base_link):
    str_in_link = "publication="
    red_act_link = requests.get(doc_base_link, allow_redirects= True)
    act_link = requests.get(doc_base_link, headers=man_headers, allow_redirects= False)
    readable_url = (urllib.parse.unquote(act_link.headers['Location']))
    act_publication_code = (readable_url[readable_url.find(str_in_link)+len(str_in_link):])
    return act_publication_code

def get_app_ip(gen_info_url):
    info_start = 'appId: "'
    info_end = '",'
    gen_info = requests.get(gen_info_url)
    slice_gen_info = (gen_info.text[gen_info.text.find(info_start)+len(info_start):])
    app_id = slice_gen_info[:slice_gen_info.find(info_end)]
    return app_id

def get_obj_id(app_id, doc_id, graphql_addr, json_headers):
    json_content = {"operationName":"CatalogPublicationQuery",
                    "variables": {"appInfo":
                                 {"appId":app_id,"appVersion":"","preview":"false"},
                                 "deviceInfo":
                                     {"deviceId":"web","deviceModel":"web","locale":"de_DE","smallestScreenWidthDp":"2337","deviceOs":"browser","platform":"web"},
                    "authorization":{"subscriptionCodes":[]},"filter":{"id":{"value":doc_id}},"first":"1"},
                    "query":"query CatalogPublicationQuery($appInfo: AppInfo!, $deviceInfo: DeviceInfo!, $authorization: Authorization!, $filter: PublicationFilter, $comparators: [PublicationComparator!], $first: Int, $after: String) {\n  catalog(\n    appInfo: $appInfo\n    deviceInfo: $deviceInfo\n    authorization: $authorization\n  ) {\n    publicationsConnection(\n      filter: $filter\n      sort: $comparators\n      first: $first\n      after: $after\n    ) {\n      pageInfo {\n        hasNextPage\n        __typename\n      }\n      totalCount\n      edges {\n        cursor\n        publication: node {\n          ...PublicationFragment\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PublicationFragment on Publication {\n  id\n  name\n  description\n  type\n  language\n  index\n  currentIssueId\n  printSubscriptionEnabled\n  freeConsumable\n  properties {\n    key\n    value\n    __typename\n  }\n  thumbnails {\n    kind\n    url\n    __typename\n  }\n  tocSettings {\n    pageLabelsEnabled\n    style\n    __typename\n  }\n  __typename\n}\n"
               }
    this_doc_id = requests.post(graphql_addr, headers = json_headers, json=json_content)
    json_doc = this_doc_id.json()
    simple_obj_link = (json_doc['data']['catalog']['publicationsConnection']['edges'][0]['publication']['currentIssueId'])
    return simple_obj_link

def get_full_obj(app_id, obj_id, graphql_addr, json_headers, auth_token):
    json_content = {"operationName":"CatalogIssuesQuery",
                "variables":{"appInfo":{"appId":app_id,"appVersion":"","preview":"false"},
                             "deviceInfo":{"deviceId":"web","deviceModel":"web","locale":"de_DE","smallestScreenWidthDp":"2337","deviceOs":"browser","platform":"web"},
                             "authorization":{"accessToken": auth_token,"subscriptionCodes":[]},
                             "filter":{"OR":[{"id":{"value": obj_id}}]}},
                "query":"query CatalogIssuesQuery($appInfo: AppInfo!, $deviceInfo: DeviceInfo!, $authorization: Authorization!, $filter: IssueFilter, $comparators: [IssueComparator!], $first: Int, $after: String) {\n  catalog(\n    appInfo: $appInfo\n    deviceInfo: $deviceInfo\n    authorization: $authorization\n  ) {\n    issuesConnection(\n      filter: $filter\n      sort: $comparators\n      first: $first\n      after: $after\n    ) {\n      pageInfo {\n        hasNextPage\n        __typename\n      }\n      totalCount\n      edges {\n        cursor\n        issue: node {\n          ...IssueFragment\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment IssueFragment on Issue {\n  id\n  version\n  name\n  description\n  index\n  alias\n  externalIssueId\n  publicationDate\n  comingSoon\n  contentLength\n  numberOfPages\n  publicationId\n  purchasable\n  productId\n  properties {\n    key\n    value\n    __typename\n  }\n  thumbnails {\n    kind\n    url\n    __typename\n  }\n  categories\n  tags\n  purchaseData {\n    purchased\n    purchasedBy\n    __typename\n  }\n  preview {\n    id\n    version\n    contentLength\n    numberOfPages\n    __typename\n  }\n  contentBundles {\n    issueVersionId\n    __typename\n  }\n  __typename\n}\n"}
    download_doc_link = requests.post(graphql_addr, headers = json_headers, json=json_content)
    json_down_doc = download_doc_link.json()
    full_doc_link = (json_down_doc['data']['catalog']['issuesConnection']['edges'][0]['issue']['properties'][0]['value'])
    return full_doc_link

def build_full_addr(app_id, obj_id, full_obj, auth_token, down_name):
    base_url = "https://epaper.mz.de/delivery/web/attachment/"
    mid_url = "?preview=false&receipt="
    end_url = "&providerType=entitlement&targetFilename="+ down_name # automatic update actual date in final version
    full_link = base_url + app_id +"/"+ obj_id + "/" + full_obj +"/" + mid_url + auth_token + end_url
    return full_link

# for example https://kiosk.purplemanager.com/mz-bitterfelder#/main/issues
# choose from list adresses
adress_for_download = addresses[3][1]
app_id = get_app_ip(gen_info_url)
doc_id = (get_doc_id(adress_for_download))
obj_id = (get_obj_id(app_id, doc_id, graphql_addr, json_headers))
auth_token = (perform_login(app_id, user_data[0][1], user_data[0][2], man_headers))
full_obj = get_full_obj(app_id, obj_id, graphql_addr, json_headers, auth_token)

down_name = str()str(datetime.now().strftime("%Y-%m-%d")) + ".pdf"
final = build_full_addr(app_id, obj_id, full_obj, auth_token, down_name)
print(final)
