import json
import math

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
    
    min_loss = min(received_powers)
    max_loss = max(received_powers)
    avg_loss = sum(received_powers) / len(received_powers)
    
    print(f"Minimum Received Power: {min_loss:.2f} dB")
    print(f"Maximum Received Power: {max_loss:.2f} dB")
    print(f"Average Received Power: {avg_loss:.2f} dB")   

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

def scale_antenna_power(reference_power, reference_size, new_size):
    """
    Scale antenna power based on new antenna size.

    Args:
        reference_power (float): Reference power in dB.
        reference_size (float): Area of the reference antenna (in m²).
        new_size (float): Area of the new antenna (in m²).

    Returns:
        float: Scaled power in dB.
    """
    scaling_factor = (new_size) / reference_size
    scaled_power = reference_power + (10 * math.log10(scaling_factor))
    return scaled_power


def calculate_path_loss_and_received_power(frequency, x0, y0, x1, y1):
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
    reference_power = -50  # Reference power in dB
    reference_transmitted_gain = 0  # Reference gain transmitted in dB
    reference_received_gain = 0  # Reference gain received in dB

    scaled_power = scale_antenna_power(reference_power, reference_size, width * height)
    
    # Convert normalized coordinates to physical dimensions
    nfc_top = y0 * average_height
    nfc_bottom = y1 * average_height
    nfc_center_y = (nfc_top + nfc_bottom) / 2

    # Receiver is a line along the width of the phone, 4 cm (0.04 m) above the top of the phone
    receiver_y = -0.04
    receiver_size = average_width * average_width

    # The shortest distance is simply the vertical distance to the receiver line
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

    power_received = scaled_power - path_loss
    return path_loss, power_received


if __name__ == "__main__":
    file_path = "nfc_positions.json"

    with open(file_path, 'r') as file:
        data = json.load(file)

    frequency = 13.56e6  # Frequency for NFC (13.56 MHz)
    results = []

    for i, item in enumerate(data):
        nfc_pos = item.get("nfcPos", {})
        path_loss, power_received = calculate_path_loss_and_received_power(frequency, nfc_pos['x0'], nfc_pos['y0'], nfc_pos['x1'], nfc_pos['y1'])
        item['path_loss'] = path_loss
        item["received_power"] = power_received
        print(f"Received Power {i}: {power_received:.2f} dB")

        results.append(item)

    # Save the results to a JSON file
    output_file = "signal_strength_results.json"
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)

    print(f"Results saved to {output_file}")
    print_received_power_stats(results)