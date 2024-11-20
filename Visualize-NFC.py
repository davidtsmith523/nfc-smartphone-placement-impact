import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json

file_path = "NfcLocalization-Android/nfcChipsOutput/nfc_positions.json"

# Load data from nfc_position.json file
with open(file_path, 'r') as file:
    data = json.load(file)

item = data[-11]
nfcPos = item.get("nfcPos", {})

# Screen dimensions (pixels)
width, height = 1080, 2400

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

ax.set_title(f"{item['marketingName']} with NFC Antenna Placement")
ax.set_xlabel("Width (pixels)")
ax.set_ylabel("Height (pixels)")

plt.show()