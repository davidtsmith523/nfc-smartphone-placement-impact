import json
import math

def print_path_loss_stats(data):
    """
    Calculate and print the minimum, maximum, and average path loss from the data.
    
    Args:
        data (list): List of dictionaries containing path loss values under the key 'path_loss'.
    """
    path_losses = [item.get('path_loss', 0) for item in data if 'path_loss' in item]
    
    if not path_losses:
        print("No path loss data available.")
        return
    
    min_loss = min(path_losses)
    max_loss = max(path_losses)
    avg_loss = sum(path_losses) / len(path_losses)
    
    print(f"Minimum Path Loss: {min_loss:.2f} dB")
    print(f"Maximum Path Loss: {max_loss:.2f} dB")
    print(f"Average Path Loss: {avg_loss:.2f} dB")


def calculate_path_loss(frequency, x0, y0, x1, y1):
    """
    Calculate the Friis path loss using average phone dimensions.

    Args:
        frequency (float): Frequency of the signal in Hz.
        x0, y0, x1, y1 (float): Normalized rectangle coordinates representing NFC position.

    Returns:
        float: Calculated path loss in dB.
    """
    # Average phone dimensions (in meters)
    average_width = 0.075  # 75 mm
    average_height = 0.15  # 150 mm

    # Convert normalized coordinates to physical dimensions
    # nfc_left = x0 * average_width
    nfc_top = y0 * average_height
    # nfc_right = x1 * average_width
    nfc_bottom = y1 * average_height

    # print(f"Left: {nfc_left:.2f}, Top: {nfc_top:.2f}, Right: {nfc_right:.2f}, Bottom: {nfc_bottom:.2f}")    

    # Calculate center of NFC rectangle
    # nfc_center_x = (nfc_left + nfc_right) / 2
    nfc_center_y = (nfc_top + nfc_bottom) / 2

    # print(f"NFC Center: ({nfc_center_x:.2f}, {nfc_center_y:.2f})")

    # Receiver is a line along the width of the phone, 4 cm (0.04 m) above the top of the phone
    receiver_y = -0.04

    # The shortest distance is simply the vertical distance to the receiver line
    distance = abs(nfc_center_y - receiver_y)
    # print(f"Distance to receiver: {distance:.4f} m")
    # print(f"Frequency: {frequency:.2f} Hz")

    # print(f"Distance to receiver: {distance:.4f} m")

    # Friis path loss formula
    c = 3e8  # Speed of light in m/s
    transmitter_gain = 0
    receiver_gain = 0
    path_loss = (
        20 * math.log10(distance) +
        20 * math.log10(frequency) -
        20 * math.log10(c / (2 * math.pi)) -
        transmitter_gain -
        receiver_gain
    )
    return path_loss


if __name__ == "__main__":
    file_path = "NfcLocalization-Android/nfcChipsOutput/nfc_positions.json"

    with open(file_path, 'r') as file:
        data = json.load(file)

    frequency = 13.56e6  # Frequency for NFC (13.56 MHz)

    results = []

    for i, item in enumerate(data):
        nfc_pos = item.get("nfcPos", {})
        path_loss = calculate_path_loss(frequency, nfc_pos['x0'], nfc_pos['y0'], nfc_pos['x1'], nfc_pos['y1'])
        # More negative dB means less path loss
        print(f"Friis Path Loss {i}: {path_loss:.2f} dB")
        # Add the path loss to the item's data
        item['path_loss'] = path_loss
        results.append(item)

    # Save the results to a JSON file
    output_file = "path_loss_results.json"
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)

    print(f"Results saved to {output_file}")
    print_path_loss_stats(results)