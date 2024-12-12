import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json

file_path = "NfcLocalization-Android/nfcChipsOutput/nfc_positions.json"

# Load data from nfc_position.json file
with open(file_path, 'r') as file:
    data = json.load(file)

item = data[26]
# item = data[-7] # Other optimal NFC placement
# item = data[-11] # Other optimal NFC placement
# item = data[26] # Other optimal NFC placement
# item = data[34] # Maximum Received Power
# item = data[75] # Minimum Received Power
# item = data[84] # Maximim Path Loss
# item = data[34] # Minimum Path Loss
nfcPos = item.get("nfcPos", {})

# Screen dimensions (mm)
width, height = 75, 150

x0, y0 = nfcPos["x0"] * width, nfcPos["y0"] * height
x1, y1 = nfcPos["x1"] * width, nfcPos["y1"] * height

fig, ax = plt.subplots(figsize=(5, 9))

# Add the NFC position rectangle
rect = patches.Rectangle(
    (x0, y0),  # Bottom-left corner
    x1 - x0,   # Width
    y1 - y0,   # Height
    linewidth=2, edgecolor='blue', facecolor='cyan', alpha=0.5
)
ax.add_patch(rect)

ax.set_xlim(0, width)
ax.set_ylim(height, 0)
ax.invert_xaxis()

ax.set_title(f"{item['marketingName']} NFC Placement")
ax.set_xlabel("Width (mm)")
ax.set_ylabel("Height (mm)")

plt.show()
