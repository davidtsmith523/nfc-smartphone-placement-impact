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

def scale_gain(reference_gain, reference_size, new_size):
    """
    Scale antenna gain based on new antenna size.

    Args:
        reference_gain (float): Reference gain in dB.
        reference_size (float): Area of the reference antenna (in m²).
        new_size (float): Area of the new antenna (in m²).

    Returns:
        float: Scaled gain in dB.
    """
    scaling_factor = new_size / reference_size
    scaled_gain = reference_gain + (10 * math.log10(scaling_factor))
    return scaled_gain


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

    reference_size = 0.002025  # Reference antenna size
    reference_transmitted_gain = 0  # Reference gain transmitted in dB
    reference_received_gain = 0  # Reference gain received in dB


    # Convert normalized coordinates to physical dimensions
    nfc_top = y0 * average_height
    nfc_bottom = y1 * average_height

    # Calculate center of NFC rectangle
    nfc_center_y = (nfc_top + nfc_bottom) / 2

    # Receiver is a line along the width of the phone, 4 cm (0.04 m) above the top of the phone
    receiver_y = -0.04
    receiver_size = average_width * average_width

    distance = abs(nfc_center_y - receiver_y)

    c = 3e8  # Speed of light in m/s
    receiver_gain = scale_gain(reference_received_gain, reference_size, receiver_size) # This will be the same every loop = 4.436974992327127
    
    # Scale the transmitted gain based on the antenna size
    transmitter_gain = scale_gain(reference_transmitted_gain, reference_size, width * height) # This will change every loop
    
    # Friis path loss formula
    path_loss = (
        20 * math.log10(distance) +
        20 * math.log10(frequency) -
        20 * math.log10(c / (4 * math.pi)) -
        transmitter_gain -
        receiver_gain
    )

    return path_loss


if __name__ == "__main__":
    file_path = "nfc_positions.json"

    with open(file_path, 'r') as file:
        data = json.load(file)

    frequency = 13.56e6  # Frequency for NFC (13.56 MHz)

    results = []

    for i, item in enumerate(data):
        nfc_pos = item.get("nfcPos", {})
        path_loss = calculate_path_loss(frequency, nfc_pos['x0'], nfc_pos['y0'], nfc_pos['x1'], nfc_pos['y1'])
        print(f"Friis Path Loss {i}: {path_loss:.2f} dB")
        item['path_loss'] = path_loss
        results.append(item)

    # Save the results to a JSON file
    output_file = "path_loss_results.json"
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)

    print(f"Results saved to {output_file}")
    print_path_loss_stats(results)
