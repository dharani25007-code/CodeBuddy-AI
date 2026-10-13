import os
import struct
import zlib

def generate_zanaks_ico(filepath):
    width = 32
    height = 32
    pixels = bytearray(width * height * 4)

    def set_pixel(x, y, r, g, b, a=255):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 4
            pixels[idx] = r
            pixels[idx + 1] = g
            pixels[idx + 2] = b
            pixels[idx + 3] = a

    # 1. Fill background with rounded shape
    for y in range(height):
        for x in range(width):
            # Distance from center
            dx = abs(x - 15.5)
            dy = abs(y - 15.5)
            # Corner distance for rounded rect (corner radius ~7)
            cx = max(0, dx - 9)
            cy = max(0, dy - 9)
            dist_sq = cx * cx + cy * cy
            if dist_sq <= 49:
                # Deep void dark blue/black
                pixels[(y * width + x) * 4 + 0] = 6
                pixels[(y * width + x) * 4 + 1] = 12
                pixels[(y * width + x) * 4 + 2] = 24
                pixels[(y * width + x) * 4 + 3] = 255
                # Border
                if dist_sq >= 30:
                    t = x / 31.0
                    r = int(0 * (1 - t) + 168 * t)
                    g = int(255 * (1 - t) + 85 * t)
                    b = int(224 * (1 - t) + 247 * t)
                    pixels[(y * width + x) * 4 + 0] = r
                    pixels[(y * width + x) * 4 + 1] = g
                    pixels[(y * width + x) * 4 + 2] = b

    # 2. Left Caliper '<'
    set_pixel(5, 13, 0, 255, 224)
    set_pixel(4, 14, 0, 255, 224)
    set_pixel(3, 15, 0, 255, 224)
    set_pixel(3, 16, 0, 255, 224)
    set_pixel(4, 17, 0, 255, 224)
    set_pixel(5, 18, 0, 255, 224)

    # 3. Right Caliper '>'
    set_pixel(26, 13, 168, 85, 247)
    set_pixel(27, 14, 168, 85, 247)
    set_pixel(28, 15, 168, 85, 247)
    set_pixel(28, 16, 168, 85, 247)
    set_pixel(27, 17, 168, 85, 247)
    set_pixel(26, 18, 168, 85, 247)

    # 4. Top bar of Z (cyan gradient)
    for x in range(9, 23):
        for y in range(8, 12):
            set_pixel(x, y, 0, 255, 224)
    for x in range(9, 23):
        set_pixel(x, 8, 255, 255, 255)  # specular highlight

    # 5. Bottom bar of Z (purple/magenta gradient)
    for x in range(9, 23):
        for y in range(20, 24):
            set_pixel(x, y, 200, 50, 230)
    for x in range(9, 23):
        set_pixel(x, 23, 255, 150, 255)

    # 6. Diagonal of Z with ridge highlight
    for step in range(12):
        t = step / 11.0
        x_c = int(21 * (1 - t) + 10 * t)
        y_c = int(11 * (1 - t) + 21 * t)
        for offset in (-1, 0, 1):
            set_pixel(x_c + offset, y_c, 100, 180, 240)
        set_pixel(x_c, y_c, 255, 255, 255)  # center specular ridge

    # 7. Quantum Diamond Core Reactor
    set_pixel(15, 14, 255, 255, 255)
    set_pixel(16, 14, 255, 255, 255)
    set_pixel(14, 15, 255, 255, 255)
    set_pixel(15, 15, 0, 255, 224)
    set_pixel(16, 15, 0, 255, 224)
    set_pixel(17, 15, 255, 255, 255)
    set_pixel(14, 16, 255, 255, 255)
    set_pixel(15, 16, 0, 255, 224)
    set_pixel(16, 16, 0, 255, 224)
    set_pixel(17, 16, 255, 255, 255)
    set_pixel(15, 17, 255, 255, 255)
    set_pixel(16, 17, 255, 255, 255)

    # Encode as PNG
    raw_lines = bytearray()
    for y in range(height):
        raw_lines.append(0)  # filter type None
        start = y * width * 4
        raw_lines.extend(pixels[start:start + width * 4])

    compressed = zlib.compress(bytes(raw_lines), 9)
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    png_data = (
        b'\x89PNG\r\n\x1a\n'
        + struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', zlib.crc32(b'IHDR' + ihdr_data))
        + struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', zlib.crc32(b'IDAT' + compressed))
        + struct.pack('>I', 0) + b'IEND' + struct.pack('>I', zlib.crc32(b'IEND'))
    )

    # Wrap into ICO format
    header = struct.pack('<HHH', 0, 1, 1)
    entry = struct.pack('<BBBBHHII', 32, 32, 0, 0, 1, 32, len(png_data), 22)
    ico_data = header + entry + png_data

    with open(filepath, 'wb') as f:
        f.write(ico_data)

    # Also save as 32x32 png
    png_path = filepath.replace('.ico', '.png')
    with open(png_path, 'wb') as f:
        f.write(png_data)

if __name__ == '__main__':
    ico_dest = os.path.join(os.path.dirname(__file__), '..', 'static', 'favicon.ico')
    generate_zanaks_ico(ico_dest)
    print('Generated:', ico_dest)
