import serial

# Configure the serial connection
serial_port = "COM6"  # Replace with your ESP32's port
baud_rate = 115200  # Match the ESP32's baud rate
output_file = "sensor_data.txt"

# Open the serial port
try:
    with serial.Serial(port=serial_port, baudrate=baud_rate, timeout=1) as ser, open(output_file, "w") as file:
        print(f"Reading data from {serial_port}... Press Ctrl+C to stop.")

        while True:
            if ser.in_waiting:  # Check if data is available
                data = ser.read(ser.in_waiting)  # Read available bytes
                hex_data = " ".join(f"{byte:02X}" for byte in data)  # Convert to hex
                print(hex_data)  # Display on the console
                file.write(hex_data + " ")  # Write to the file
except KeyboardInterrupt:
    print("\nExiting...")
except Exception as e:
    print(f"Error: {e}")
