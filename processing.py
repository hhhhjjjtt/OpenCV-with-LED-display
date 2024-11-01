import cv2 as cv
import serial

# To check: first open device manager, then look for 'Ports'
# and see which port Arduino is connected to
ser = serial.Serial('COM8', 9600)

# Compress a video frame to 8*8 binary freme
def rescale_to_8_8_binary(frame, threshold=127):
    frame = cv.resize(frame, (8, 8), interpolation=cv.INTER_AREA)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    _, binary_frame = cv.threshold(gray_frame, threshold, 1, cv.THRESH_BINARY)
    return binary_frame

# Convert frame to binary array
def binary_frame_to_bytes(binary_frame):
    byte_array = []
    for row in binary_frame:
        byte = 0
        for bit in row:
            byte = (byte << 1) | bit
        byte_array.append(byte)
    return byte_array

capture = cv.VideoCapture('bad_apple.mp4')

print("Press \"d\" to stop")

while True:
    isTrue, frame = capture.read()
    if not isTrue:
        break

    # Process each frame
    binary_frame = rescale_to_8_8_binary(frame)
    frame_bytes = binary_frame_to_bytes(binary_frame)

    # Transmit frame bytes to Arduino
    ser.write(bytearray(frame_bytes))

    enlarged_frame = cv.resize(binary_frame * 255, (160, 160), interpolation=cv.INTER_NEAREST)
    cv.imshow('Enlarged 8x8 Video', enlarged_frame)
    cv.imshow('original Video', frame)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

# Clear the LED when progress finished
empty_screen = [0] * 64
ser.write(bytearray(empty_screen))

capture.release()
ser.close()
cv.destroyAllWindows()