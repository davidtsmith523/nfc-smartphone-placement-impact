import json

file_path = "NfcLocalization-Android/nfcChipsOutput/nfc_positions.json"
# Top of the phone is at y = 1 (normalized)
top_of_phone_y = 1

# Load data from nfc_position.json file
with open(file_path, 'r') as file:
    data = json.load(file)

# Loop through each item in the data and print the NFC position
for item in data:
    nfc_pos = item.get("nfcPos", {})
    print(f"NFC Position for {item['marketingName']}: {nfc_pos}")
    # Calculate the distance from the NFC position to the top of the phone
    distance_to_top_1 = top_of_phone_y - nfc_pos['y0']
    distance_to_top_2 = top_of_phone_y - nfc_pos['y1']
    # Print the distances
    print(f"Distance from NFC position (x0, y0) to top of phone: {distance_to_top_1:.4f} units")
    print(f"Distance from NFC position (x1, y1) to top of phone: {distance_to_top_2:.4f} units")

