import cv2
import numpy as np

# Create a blank image
image = np.ones((200, 600), dtype=np.uint8) * 255

# Set the text to draw
text = "Hello, Tesseract OCR!"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2

# Get the text size
text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

# Calculate the text position
text_x = (image.shape[1] - text_size[0]) // 2
text_y = (image.shape[0] + text_size[1]) // 2

# Put the text on the image
cv2.putText(image, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness)

# Save the image
cv2.imwrite('created.png', image)
