import requests
import json
from datetime import datetime, timedelta

def api_login():
    # I focussed on the application_login()-example, thus I recommend to look further below.
    req = requests.Session()
    with open("ovc_url.json", "r") as ovc_data:
        ovc_url = json.load(ovc_data)
        ovc_url = ovc_url.rtrim("/")
    with open("ovc_settings.json", "r") as login_data:
        login_json = json.load(login_data)
    resp = req.post(f"{ovc_url}/api/user/signin", json=login_json)
    #print(json.dumps(resp.json(), indent=4))    
    user_profile = req.get(f"{ovc_url}/api/ov/v1/user/profile")
    print(json.dumps(user_profile.json(), indent=4))
    user_organizations = req.get(f"{ovc_url}/api/ov/v1/organizations/permissions")
    print(json.dumps(user_organizations.json(), indent=4))
    user_sites = req.get(f"{ovc_url}/api/ov/v1/sites/permissions")
    print(json.dumps(user_sites.json(), indent=4))
    #user_sites = user_sites.json()
    #print(user_sites["data"][0]["id"])
    # organization & site, not the IDs
    #devices = req.get(f"{ovc_url}/api/ov/v1/organizations/623a6138b05dd4a8ecbe92fe/sites/623a62c9b05dd40f99be930b/devices")
    devices = req.get(f"{ovc_url}/api/ov/v1/organizations/{user_organizations.json()['data'][0]['organization']}/sites/{user_sites.json()['data'][0]['site']}/devices")
    print(json.dumps(devices.json(), indent=4))

def application_login():
    req = requests.Session()
    with open("ovc_url.json", "r") as ovc_data:
        ovc_url = json.load(ovc_data)
        ovc_url = ovc_url["ovc_url"].rstrip("/")
    with open("ovc_application_settings.json", "r") as login_data:
        login_json = json.load(login_data)
    resp = req.post(f"{ovc_url}/api/ov/v1/applications/authenticate", json=login_json)
    print("### /api/ov/v1/applications/authenticate - Access Token ###")
    #print(json.dumps(resp.json(), indent=4))
    print("REDACTED")
    ov_header =  {"Content-Type": "application/json"}
    ov_header["Authorization"] = f"Bearer {resp.json()['access_token']}"
    user_profile = req.get(f"{ovc_url}/api/ov/v1/user/profile", headers=ov_header)
    print("### /api/ov/v1/user/profile - User Profile ###")
    #print(json.dumps(user_profile.json(), indent=4))
    print("REDACTED")
    user_organizations = req.get(f"{ovc_url}/api/ov/v1/organizations/permissions", headers=ov_header)
    print("### /api/ov/v1/organizations/permissions - Organisation Permissions ###")
    print(json.dumps(user_organizations.json(), indent=4))
    user_sites = req.get(f"{ovc_url}/api/ov/v1/sites/permissions", headers=ov_header)  
    print("### /api/ov/v1/sites/permissions - Sites Permissions ###")
    print(json.dumps(user_sites.json(), indent=4))
    for current_site in user_sites.json()['data']:
        site = req.get(f"{ovc_url}/api/ov/v1/organizations/{user_organizations.json()['data'][0]['organization']}/sites/{current_site['site']}", headers=ov_header)
        print("### /api/ov/v1/organizations/<ORGANISATION>/sites/<SITE> - Site: Details ###")
        print(json.dumps(site.json(), indent=4))
        #user_sites = user_sites.json()
        #print(user_sites["data"][0]["id"])
        print(f"### Getting Devices for {site.json()['data']['name']} ###")
        # organization & site, not the IDs
        devices = req.get(f"{ovc_url}/api/ov/v1/organizations/{user_organizations.json()['data'][0]['organization']}/sites/{current_site['site']}/devices", headers=ov_header)
        if devices.json()["data"]:
            print("### /api/ov/v1/organizations/<ORGANISATION>/sites/<SITE>/devices - Site: Devices ###")
            print(json.dumps(devices.json(), indent=4))
            for current_device in devices.json()["data"]:
                last_hour_date_time = datetime.now() - timedelta(hours = 1)
                client_query = {
                    # 2021-03-28T00:00:00+01:00
                    "startDate":f"{last_hour_date_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')}",
                    "endDate":f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')}", 
                    "scope":"ap",
                    "scopeId[]":[current_device['macAddress']]
                }
                # Note that this GET leverages "params"
                client_list = req.get(f"{ovc_url}/api/ov/v1/organizations/{user_organizations.json()['data'][0]['organization']}/wlan-analytics/client-analytics/client-list", headers=ov_header, params=client_query)
                print(f"### Getting Clients ###")
                if client_list.json()["data"]:
                    print(json.dumps(client_list.json(), indent=4))
                else:
                    print("No connected clients!")
                
                last_hour_date_time = datetime.now() - timedelta(hours = 12)
                iot_query = {
                    # 2021-09-22T04:30:00.000Z
                    "startDate":f"{last_hour_date_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}",
                    "endDate":f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')}",
                    "latest":"true",
                    "limit":10,
                    "offset":0,
                    "scope":"ap",
                    "scopeId[]":[current_device['macAddress']]
                }
                #print(iot_query)
                # Note that this GET leverages "params"
                iot_list = req.get(f"{ovc_url}/api/ov/v1/organizations/{user_organizations.json()['data'][0]['organization']}/iot/inventory", headers=ov_header, params=iot_query)
                print(f"### Getting IoT ###")
                if iot_list.json()["data"]["result"]:
                    print(json.dumps(iot_list.json(), indent=4))
                else:
                    print("No IoT clients detected!")                    
        else:
            print("No devices on this site!")
            continue

if __name__ == "__main__":
    # login token is valid for 12 hours
    #api_login()
    # application token is valid for 15 days
    # application token login will probably not require 2FA
    application_login()
