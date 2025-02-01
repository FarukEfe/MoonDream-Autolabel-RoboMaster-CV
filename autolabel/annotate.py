# Work with Moondream
import moondream as md
import argparse, os, ntpath
from dotenv import load_dotenv
from PIL import Image
# Setup & Model
load_dotenv()
model = md.vl(api_key=os.getenv('API_KEY'))

# MARK: Helper Methods

# Load the image
def open_img(dir):
    image = Image.open(dir)
    w, h = image.width, image.height
    return image, w, h

# Compute absolute coordinates
def pixel_coords(point, w, h):
    acc_x, acc_y = w * point["x"], h * point["y"]
    #print(f"Norm: ({point["x"]}, {point["y"]}) |---| Actual: ({acc_x}, {acc_y})")
    return acc_x, acc_y

# MARK: Moondream Calls

# Get Bounding Box from Image
def bbox(img):
    pass
# Get Center Point from Image
def cpoint(img):
    query = "Square-shaped black armor plate on a robot with a number on it and 2 LED lights on the sides"
    points = model.point(img, query)["points"]
    return points[0] # For now we only care about the top guess

# Get red or blue tag
def tag(img):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Moondream Annotator')
    # Add flags & parse arguments
    parser.add_argument('-f', '--folder', type=str, help='Folder directory to image dataset')
    args = parser.parse_args()
    # Error Handling
    ds_dir: str = os.path.abspath(args.folder)
    if not os.path.exists(ds_dir):
        print("Dataset folder not found.")
        exit(1)
    # Label Dataset
    dirs = [os.path.join(ds_dir, f) for f in os.listdir(ds_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    file = open(os.path.join(ds_dir, 'annotation.txt'), 'w')
    for dir in dirs:
        head, tail = ntpath.split(dir)
        print(f'Labeling {tail}')
        img, w, h = open_img(dir)
        pts = cpoint(img)
        acc_x, acc_y = pixel_coords(pts, w, h)
        file.write(f"{tail},{acc_x},{acc_y}\n")
    file.close()