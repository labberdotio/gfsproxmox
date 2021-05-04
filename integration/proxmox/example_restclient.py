import requests

url = "https://192.168.0.180:8006/api2/json/nodes/botcore/qemu/109/status/current"
# url = "http://192.168.0.160:18006/api2/json/nodes/botcore/qemu/109/status/current"

headers = {
    'user-agent': "vscode-restclient",
    'content-type': "application/json",
    'authorization': "PVEAPIToken=bots@pam!botcanics=bc1f0af3-49f1-41a2-8729-003e99ec3625"
    }

response = requests.request("GET", url, headers=headers, verify=False)

print(response.text)