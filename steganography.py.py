from PIL import Image

# Convert text to binary
def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

# Convert binary to text
def binary_to_text(binary_data):
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

# Hide the message in the image
def hide_message(input_image_path, output_image_path, secret_message):
    image = Image.open(input_image_path)
    
    # Ensure image is in RGB mode
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert message to binary and add an end delimiter
    binary_message = text_to_binary(secret_message) + '1111111111111110'
    
    message_index = 0
    pixels = list(image.getdata())
    new_pixels = []

    for pixel in pixels:
        r, g, b = pixel
        if message_index < len(binary_message):
            r = (r & ~1) | int(binary_message[message_index])
            message_index += 1
        if message_index < len(binary_message):
            g = (g & ~1) | int(binary_message[message_index])
            message_index += 1
        if message_index < len(binary_message):
            b = (b & ~1) | int(binary_message[message_index])
            message_index += 1
        new_pixels.append((r, g, b))

    if message_index < len(binary_message):
        raise ValueError("Message is too long to hide in this image.")

    image.putdata(new_pixels)
    image.save(output_image_path)
    print(f"Secret message hidden and saved as '{output_image_path}'.")

# Reveal the message from the image
def reveal_message(encoded_image_path):
    image = Image.open(encoded_image_path)
    pixels = list(image.getdata())
    binary_data = ''

    for pixel in pixels:
        for color in pixel[:3]:
            binary_data += str(color & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]

    hidden_message = ''
    for byte in all_bytes:
        if byte == '11111110':
            break
        hidden_message += chr(int(byte, 2))
    return hidden_message

# Main execution
if __name__ == "__main__":
    original_image = "input.png"
    stego_image = "output.png"
    message = "This is a hidden message."

    hide_message(original_image, stego_image, message)

    recovered = reveal_message(stego_image)
    print("Recovered message:", recovered)
