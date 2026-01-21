import cv2
import numpy as np

# Color database (RGB)
COLORS = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Gray": (128, 128, 128),
    "Orange": (255, 165, 0),
    "Pink": (255, 192, 203),
    "Purple": (128, 0, 128),
    "Brown": (165, 42, 42)
}

def get_color_name(rgb):
    min_dist = float("inf")
    color_name = "Unknown"
    detected_rgb = (0, 0, 0)

    for name, value in COLORS.items():
        dist = np.sqrt(sum((rgb[i] - value[i]) ** 2 for i in range(3)))
        if dist < min_dist:
            min_dist = dist
            color_name = name
            detected_rgb = value

    return color_name, detected_rgb

# Open camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2

    # Get center pixel (BGR)
    pixel = frame[cy, cx]
    rgb = (int(pixel[2]), int(pixel[1]), int(pixel[0]))

    color_name, color_rgb = get_color_name(rgb)

    # Convert RGB to BGR for OpenCV
    box_color = (color_rgb[2], color_rgb[1], color_rgb[0])

    # Draw ONLY the box border (no fill)
    cv2.rectangle(
        frame,
        (cx - 30, cy - 30),
        (cx + 30, cy + 30),
        box_color,
        3  # border thickness
    )

    # Display text
    cv2.putText(frame, f"Color: {color_name}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, box_color, 2)

    cv2.putText(frame, f"RGB: {rgb}",
                (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, box_color, 2)

    cv2.imshow("Color Identifier", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
