import json
import math

def scale_antenna_power(reference_power_dB, reference_size, new_size):
    """
    Scale antenna power based on new antenna size.

    Args:
        reference_power_dB (float): Reference power in dB.
        reference_size (float): Area of the reference antenna (in m²).
        new_size (float): Area of the new antenna (in m²).

    Returns:
        float: Scaled power in dB.
    """
    scaling_factor = (new_size * 0.8) / reference_size
    scaled_power_dB = reference_power_dB + 10 * math.log10(scaling_factor)
    print(f"Scaling Factor: {scaling_factor:.2f}")
    return scaled_power_dB


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

def print_received_power_stats(data):
    """
    Calculate and print the minimum, maximum, and average received power from the data.
    
    Args:
        data (list): List of dictionaries containing received power values under the key 'received_power'.
    """
    received_powers = [item.get('received_power', 0) for item in data if 'received_power' in item]
    
    if not received_powers:
        print("No received power data available.")
        return
    
    min_power = min(received_powers)
    max_power = max(received_powers)
    avg_power = sum(received_powers) / len(received_powers)
    
    print(f"Minimum Received Power: {min_power:.2f} dB")
    print(f"Maximum Received Power: {max_power:.2f} dB")
    print(f"Average Received Power: {avg_power:.2f} dB")   


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

    width = (x1 - x0) * average_width
    height = (y1 - y0) * average_height
    # print(f"Width: {width:.2f} m, Height: {height:.2f} m")

    scaled_power = scale_antenna_power(-50, 0.001225, width * height)
    # Calculate received signal strength in dB

    # Convert normalized coordinates to physical dimensions
    nfc_top = y0 * average_height
    nfc_bottom = y1 * average_height

    # Calculate center of NFC rectangle
    nfc_center_y = (nfc_top + nfc_bottom) / 2

    # Receiver is a line along the width of the phone, 4 cm (0.04 m) above the top of the phone
    receiver_y = -0.04

    # The shortest distance is simply the vertical distance to the receiver line
    distance = abs(nfc_center_y - receiver_y)

    # Friis path loss formula
    c = 3e8  # Speed of light in m/s
    transmitter_gain = 0
    receiver_gain = 0
    path_loss = (
        20 * math.log10(distance) +
        20 * math.log10(frequency) - 
        20 * math.log10(c / (4 * math.pi)) - 
        transmitter_gain - 
        receiver_gain
    )

    P_r_dB = scaled_power - path_loss
    return path_loss, P_r_dB


if __name__ == "__main__":
    file_path = "NfcLocalization-Android/nfc_positions.json"

    with open(file_path, 'r') as file:
        data = json.load(file)

    frequency = 13.56e6  # Frequency for NFC (13.56 MHz)

    results = []

    for i, item in enumerate(data):
      nfc_pos = item.get("nfcPos", {})
      path_loss, P_r_dB = calculate_path_loss(frequency, nfc_pos['x0'], nfc_pos['y0'], nfc_pos['x1'], nfc_pos['y1'])
      print(f"Friis Path Loss {i}: {path_loss:.2f} dB")
      print(f"Received Power {i}: {P_r_dB:.2f} dB")
      # Add the path loss to the item's data
      item['path_loss'] = path_loss
      item["received_power"] = P_r_dB
      results.append(item)

    # Save the results to a JSON file
    output_file = "path_loss_results.json"
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)

    print(f"Results saved to {output_file}")
    print_path_loss_stats(results)
    print_received_power_stats(results)
