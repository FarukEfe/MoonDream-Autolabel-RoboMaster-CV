import moondream as md
from PIL import Image
# Moondream key
from PERSONAL import API_KEY

# Initialize the model with your API key
model = md.vl(api_key=API_KEY)

# Load the image
image = Image.open("./frames/macu_vs_uofa/fps/frame00660.jpg")
w, h = image.width, image.height
print(f"Image dims are: {w}x{h}")

# Get center points of object
object_name = "Number"
points = model.point(image, object_name)["points"]

# Output the results (moondream returns normalized coordinates)
for point in points:
    acc_x, acc_y = w * point["x"], h * point["y"] # Pixel Coordinates
    print(f"Norm: ({point['x']}, {point['y']}) |---| Actual: ({acc_x}, {acc_y})")

