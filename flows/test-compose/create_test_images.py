from PIL import Image, ImageDraw, ImageFont

# Create 3 simple test images with different colors
colors = [
    (255, 0, 0, 255),    # Red
    (0, 255, 0, 255),    # Green
    (0, 0, 255, 255),    # Blue
]

for i, color in enumerate(colors):
    img = Image.new('RGBA', (200, 200), color)
    draw = ImageDraw.Draw(img)

    # Draw frame number
    text = f"Frame {i+1}"
    # Use default font
    bbox = draw.textbbox((0, 0), text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = ((200 - text_width) // 2, (200 - text_height) // 2)
    draw.text(position, text, fill=(255, 255, 255, 255))

    img.save(f"/tmp/test_frame_{i+1}.png")

print("Created test images:")
for i in range(3):
    print(f"/tmp/test_frame_{i+1}.png")
