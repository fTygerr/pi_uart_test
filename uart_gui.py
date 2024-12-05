import tkinter as tk
import serial
import os
import time  # Import time for delays

# Suppress tkinter deprecation warning
os.environ["TK_SILENCE_DEPRECATION"] = "1"

# Toggle state for vending machine
vending_state = {"state": "OFF"}

def toggle_vending_machine():
    """
    Toggles the state of the vending machine between ON and OFF,
    sends the appropriate command, and logs the response.
    """
    # Choose command based on the vending machine state
    command = "VON\r" if vending_state["state"] == "OFF" else "VOFF\r"
    print(f"[DEBUG] Current state: {vending_state['state']}")
    print(f"[DEBUG] Sending command: {command.strip()} (with CR)")

    # Send command
    ser.write(command.encode())
    print(f"[LOG] Sent command: {command.strip()}")

    # Update the state
    if vending_state["state"] == "OFF":
        vending_state["state"] = "ON"
        output_label.config(text="Vending Machine: ON")
    else:
        vending_state["state"] = "OFF"
        output_label.config(text="Vending Machine: OFF")

    # Add a delay to ensure the hardware processes the command
    time.sleep(1)

    # Check for response
    print(f"[DEBUG] Bytes waiting in buffer: {ser.in_waiting}")
    if ser.in_waiting:
        # Read the raw response from the buffer
        raw_response = ser.read(ser.in_waiting)
        print(f"[DEBUG] Raw response bytes: {raw_response}")

        # Decode the raw response
        response = raw_response.decode().strip()
        print(f"[LOG] Received response: {response}")

        if response == "ERR":
            print("[ERROR] Received error response from hardware.")
        elif response in ["VON", "VOFF"]:
            print(f"[LOG] Hardware echoed back: {response}")
        else:
            print(f"[WARNING] Unexpected response: {response}")
    else:
        print("[WARNING] No response received from hardware.")

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

# GUI Setup
root = tk.Tk()
root.title("UART Communicator - Vending Machine")

frame = tk.Frame(root)
frame.pack()

# Button to toggle vending machine state
toggle_button = tk.Button(frame, text="Toggle Vending Machine", command=toggle_vending_machine)
toggle_button.pack()

# Output label to show the current state
output_label = tk.Label(root, text="Vending Machine: OFF")
output_label.pack()

print("[LOG] GUI initialized. Ready for interaction.")
root.mainloop()