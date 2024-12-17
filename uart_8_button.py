import tkinter as tk
import serial
import os
import time

# Suppress tkinter deprecation warning
os.environ["TK_SILENCE_DEPRECATION"] = "1"

# Setup serial communication
try:
    ser = serial.Serial(
        port='/dev/serial0',  # Default UART for Raspberry Pi Zero 2 W
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )
    print("[LOG] Using hardware UART at /dev/serial0.")
except serial.serialutil.SerialException as e:
    print(f"[ERROR] Failed to initialize UART: {e}")
    exit(1)

# Key configuration
KEY_PRESS_DURATION = "1000"  # Default milliseconds duration for key closure
KEY_LABELS = [
    "Key 0", "Key 1", "Key 2", "Key 3",
    "Key 4", "Key 5", "Key 6", "Key 7"
]

# Command execution function
def send_key_command(key_number):
    """
    Sends a KEY command to the hardware for a specific key number.

    Parameters:
        key_number (int): The key number (0 to 7)
    """
    command = f"KEY {key_number} {KEY_PRESS_DURATION}\r"
    print(f"[DEBUG] Sending command: {command.strip()}")

    try:
        ser.write(command.encode())
        time.sleep(0.5)  # Allow time for hardware response

        # Check response
        if ser.in_waiting:
            response = ser.read(ser.in_waiting).decode().strip()
            print(f"[LOG] Received response: {response}")
            if response == "ACK":
                key_labels[key_number].config(text=f"Key {key_number}: ACK")
            elif response == "NACK":
                key_labels[key_number].config(text=f"Key {key_number}: NACK")
            else:
                key_labels[key_number].config(text=f"Key {key_number}: UNKNOWN")
        else:
            print("[WARNING] No response received from hardware.")
            key_labels[key_number].config(text=f"Key {key_number}: No Response")
    except Exception as e:
        print(f"[ERROR] Failed to send command: {e}")
        key_labels[key_number].config(text=f"Key {key_number}: Error")

# GUI Setup
root = tk.Tk()
root.title("UART Communicator - Keypad Interface")

frame = tk.Frame(root)
frame.pack()

# Create buttons and labels for 2x4 grid
buttons = []
key_labels = []

for i in range(8):  # 8 keys (0-7)
    row = i // 4
    col = i % 4

    # Button for each key
    button = tk.Button(frame, text=KEY_LABELS[i], width=12, height=2, command=lambda n=i: send_key_command(n))
    button.grid(row=row * 2, column=col, padx=5, pady=5)
    buttons.append(button)

    # Label below each button for feedback
    label = tk.Label(frame, text=f"Key {i}: Waiting")
    label.grid(row=row * 2 + 1, column=col, padx=5, pady=2)
    key_labels.append(label)

print("[LOG] GUI initialized. Ready for interaction.")
root.mainloop()