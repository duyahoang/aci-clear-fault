import databaseconfig_aci as cfg
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def login():

    url = "https://{}/api/aaaLogin.json".format(
        cfg.apic_info["apic_ip_address"])

    payload = {
        "aaaUser": {
            "attributes": {
                "name": cfg.apic_info["username"],
                "pwd": cfg.apic_info["password"]
            }
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(
        payload), headers=headers, verify=False).json()

    # print(json.dumps(response, indent=2)

    token = response["imdata"][0]["aaaLogin"]["attributes"]["token"]
    cookie = dict()
    cookie["APIC-cookie"] = token

    # print(cookie)

    return cookie


def is_IgnoreAckedFaults():

    url = "https://{}/api/mo/uni/fabric/hsPols/hseval.json".format(
        cfg.apic_info["apic_ip_address"])

    cookie = login()

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers,
                            cookies=cookie, verify=False).json()

    if response["imdata"][0]["healthEvalP"]["attributes"]["ignoreAckedFaults"] == "no":
        ignoreAckedFaults = False
    else:
        ignoreAckedFaults = True

    # print(response["imdata"][0]["healthEvalP"]
    #       ["attributes"]["ignoreAckedFaults"])
    # print(ignoreAckedFaults)

    return ignoreAckedFaults


def on_IgnoreAckedFaults():
    url = "https://{}/api/mo/uni/fabric/hsPols/hseval.json".format(
        cfg.apic_info["apic_ip_address"])

    cookie = login()

    headers = {
        "Content-Type": "application/json"
    }

    payload = {"healthEvalP": {"attributes": {"dn": "uni/fabric/hsPols/hseval",
                                              "ignoreAckedFaults": "true"}}}

    response = requests.post(url, headers=headers, data=json.dumps(
        payload), cookies=cookie, verify=False).json()

    print(json.dumps(response, indent=2))


def off_IgnoreAckedFaults():
    url = "https://{}/api/mo/uni/fabric/hsPols/hseval.json".format(
        cfg.apic_info["apic_ip_address"])

    cookie = login()

    headers = {
        "Content-Type": "application/json"
    }

    payload = {"healthEvalP": {"attributes": {"dn": "uni/fabric/hsPols/hseval",
                                              "ignoreAckedFaults": "false"}}}

    response = requests.post(url, headers=headers, data=json.dumps(
        payload), cookies=cookie, verify=False).json()

    # print(json.dumps(response, indent=2))


def main():

    cookie = login()
    print(is_IgnoreAckedFaults())
    if not is_IgnoreAckedFaults():
        on_IgnoreAckedFaults()

    print(is_IgnoreAckedFaults())


main()
