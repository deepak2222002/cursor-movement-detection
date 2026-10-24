from pynput import mouse, keyboard
import winsound
import threading
import time

alarm_running = False
lock = threading.Lock()


def play_alarm():
    global alarm_running

    with lock:
        if alarm_running:
            return
        alarm_running = True

    print("⚠️ INPUT DETECTED! ALARM!")

    # Play alarm repeatedly
    for i in range(5):
        winsound.Beep(3000, 500)
        time.sleep(0.1)

    with lock:
        alarm_running = False


def input_detected():
    # Run alarm in separate thread so monitoring doesn't stop
    threading.Thread(target=play_alarm, daemon=True).start()


# Mouse movement
def on_move(x, y):
    input_detected()


# Mouse click
def on_click(x, y, button, pressed):
    if pressed:
        input_detected()


# Mouse scroll
def on_scroll(x, y, dx, dy):
    input_detected()

# Keyboard
def on_press(key):
    input_detected()


print("===================================")
print(" Input Monitoring Started")
print(" Monitoring mouse + keyboard")
print(" Press Ctrl+C to stop")
print("===================================")

# Start mouse listener
mouse_listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll
)

# Start keyboard listener
keyboard_listener = keyboard.Listener(
    on_press=on_press
)

mouse_listener.start()
keyboard_listener.start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
    mouse_listener.stop()
    keyboard_listener.stop()