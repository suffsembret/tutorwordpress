import requests

api_address = "http://10.24.24.7:7557"

def gantissid(data, ssid):
    print("acs:", data["sn"])
    try:
        parameter = {
            "name": "setParameterValues",
            "parameterValues": [
                ["InternetGatewayDevice.LANDevice.1.WLANConfiguration.4.SSID", ssid, "xsd:string"]
            ]
        }
        response = requests.post(f'{api_address}/devices/{data["sn"]}/tasks?connection_request', json=parameter)
        print(response.status_code)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return 500
def gantipw(data, pw):
  print("acs:", data["sn"])
  try:
    parameter = {
      "name": "setParameterValues",
            "parameterValues": [
              ["InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.PreSharedKey.1.PreSharedKey", pw , "xsd:string"]
           ]
        }
        response = requests.post(f'{api_address}/devices/{data["sn"]}/tasks?connection_request', json=parameter)
        print(response.status_code)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return 500
# 
    
    
  
