import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json

file_path = "NfcLocalization-Android/nfcChipsOutput/nfc_positions.json"

with open(file_path, 'r') as file:
    data = json.load(file)


# item = data[34]
item = data[84]
# item = data[26]
nfcPos = item.get("nfcPos", {})

# Phone dimensions (normalized)
phone_width = 1
phone_height = 1

fig, ax = plt.subplots(figsize=(6, 8))

phone = patches.Rectangle((0, 0), phone_width, phone_height, linewidth=2, edgecolor='blue', facecolor='lightblue', label="Phone")
ax.add_patch(phone)

print(nfcPos)

nfc_antenna = patches.Rectangle((nfcPos['x0'], nfcPos['y0']), 
                                nfcPos['x1'] - nfcPos['x0'], 
                                nfcPos['y1'] - nfcPos['y0'], 
                                linewidth=2, edgecolor='green', facecolor='lightgreen', label="NFC Antenna")
ax.add_patch(nfc_antenna)

ax.plot([0, phone_width], [0, 0], color="red", linestyle="-", label="Top of Phone")

ax.set_title(f"{item['marketingName']} with NFC Antenna Placement")
ax.set_xlabel("X-axis (Normalized)")
ax.set_ylabel("Y-axis (Normalized)")
ax.set_xlim(0, phone_width)
ax.set_ylim(0, phone_height)

ax.invert_yaxis()
ax.spines['top'].set_color('red')
ax.invert_xaxis()

ax.legend(loc="lower left")

plt.show()