import serial
import csv
import struct
import time

# Configuration
serial_port = "COM6"  # Adjust as per your system
baud_rate = 256000  # Default baud rate
output_csv = "ld2450_data.csv"
frame_rate = 10  # Frames per second

# Define frame format
FRAME_HEADER = b"\xAA\xFF\x03\x00"
FRAME_END = b"\x55\xCC"

# Function to parse a single frame
def parse_frame(frame):
    try:
        # Verify header and footer
        if not frame.startswith(FRAME_HEADER) or not frame.endswith(FRAME_END):
            print("Invalid frame header or footer")
            return None

        # Extract intra-frame data (14 bytes for one target as per Table 3)
        target_data = frame[4:-2]
        if len(target_data) < 14:
            print("Invalid frame length")
            return None

        # Parse fields
        x, y, speed, distance = struct.unpack(">hhhh", target_data[:8])

        # Return parsed data
        return {
            "Target X Coordinate": x,
            "Target Y Coordinate": y,
            "Target Speed": speed,
            "Distance Resolution": distance,
            "Complete Data String": frame.hex().upper(),
        }
    except Exception as e:
        print(f"Error parsing frame: {e}")
        return None

# Main function to read data and save to CSV
def read_and_save_to_csv():
    try:
        with serial.Serial(serial_port, baudrate=baud_rate, timeout=1) as ser, open(output_csv, "w", newline="") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=[
                    "Timestamp",
                    "Target X Coordinate",
                    "Target Y Coordinate",
                    "Target Speed",
                    "Distance Resolution",
                    "Complete Data String",
                ],
            )
            writer.writeheader()

            print(f"Listening on {serial_port} at {baud_rate} baud...")
            while True:
                time.sleep(0.1 / frame_rate)  # Wait for the next frame
                if ser.in_waiting >= 18:  # Minimum frame size is 18 bytes
                    raw_data = ser.read(18)
                    parsed_data = parse_frame(raw_data)
                    if parsed_data:
                        parsed_data["Timestamp"] = time.time()
                        writer.writerow(parsed_data)
                        print(parsed_data)
                    else:
                        print("Invalid frame received")
                else:
                    print("Doesn't have enough data to read a frame")
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"Error: {e}")

# Run the script
read_and_save_to_csv()
