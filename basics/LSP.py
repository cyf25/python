from PIL import Image

def str_to_bin(data):
    return ''.join(format(byte, '08b') for byte in data.encode('utf-8'))

def bin_to_str(binary_data):
    bytes_data = bytearray()
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if byte == '00000000':
            break
        bytes_data.append(int(byte, 2))
    return bytes_data.decode('utf-8')

def hide_data(img_path, output_path, secret_data):
    img = Image.open(img_path).convert("RGB")
    binary_secret = str_to_bin(secret_data) + '00000000'  # UTF-8结束符
    pixels = list(img.getdata())
    new_pixels = []
    data_index = 0

    for pixel in pixels:
        r, g, b = pixel
        new_rgb = []

        for color in (r, g, b):
            if data_index < len(binary_secret):
                color = (color & ~1) | int(binary_secret[data_index])
                data_index += 1
            new_rgb.append(color)

        new_pixels.append(tuple(new_rgb))

    img.putdata(new_pixels)
    img.save(output_path)
    print("✅ 中文信息已隐藏至：", output_path)

def extract_data(img_path):
    img = Image.open(img_path).convert("RGB")
    binary_data = ''
    for pixel in img.getdata():
        for value in pixel[:3]:
            binary_data += str(value & 1)

    return bin_to_str(binary_data)

if __name__ == '__main__':
    name = "程允锋"
    student_id = "2220228013"
    secret = f"姓名: {name}\n学号: {student_id}"

    original_image = r"basics\original.jpg"
    encoded_image = "encrypt_image.png"

    hide_data(original_image, encoded_image, secret)

    print("🕵️ 提取信息中...")
    result = extract_data(encoded_image)
    print("🎯 提取结果：")
    print(result)
