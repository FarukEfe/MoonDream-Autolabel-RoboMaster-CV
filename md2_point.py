# Work with Moondream
import moondream as md
import cv2, numpy as np, os
from PIL import Image, ImageFile, ImageDraw
# Moondream key
from PERSONAL import API_KEY

# Initialize the model with your API key
model = md.vl(api_key=API_KEY)

# Load the image
def open_img(dir):
    image = Image.open(dir)
    w, h = image.width, image.height
    return image, w, h

# Get center points of object "Number on Robot"
def get_annotation(img):
    points = model.point(img, "Number on robot")["points"]
    #cls = model.query(img, 'Is the robot red or blue? Return answer in lowercase.')
    return points#, cls

# Output the results (moondream returns normalized coordinates)
# FIX: THIS DOESN'T RETURN ALL POINT PREDICTIONS, JUST THE LAST ONE SO FIX IT!
def compute_pixel_coords(points, w, h):
    norm_x, norm_y = 0, 0
    acc_x, acc_y = 0, 0
    for point in points:
        norm_x, norm_y = point["x"], point["y"]
        acc_x, acc_y = w * norm_x, h * norm_y # Pixel Coordinates
        print(f"Norm: ({norm_x}, {norm_y}) |---| Actual: ({acc_x}, {acc_y})")
    return acc_x, acc_y

# Check correctness
def user_verify(image, acc_x, acc_y) -> int:
    copied = image.copy()
    # draw on image
    draw = ImageDraw.Draw(copied)
    color = (0, 0, 0)
    draw.line((0,0,acc_x,acc_y), fill=color)
    # use opencv to display
    opencv_image = cv2.cvtColor(np.array(copied), cv2.COLOR_RGB2BGR)
    cv2.imshow('image', opencv_image)
    # Wait for user key
    while True:
        key = cv2.waitKey(0) & 0xFF # Wait indefinitely for a key press
        if key == ord('e'):  # Accept image and label if key is E
            cv2.destroyAllWindows()
            return True
        elif key == ord('r'):  # Reject image and label if key is R
            cv2.destroyAllWindows()
            return False
        else:
            exit(0)

# Save in storage
def save_with_labels(img, acc_x, acc_y, dest: str):
    '''
    path_blue = os.path.join(dest, 'blue')
    path_red = os.path.join(dest, 'red')
    count_blue = len([f for f in os.listdir(path_blue) if os.path.isfile(os.path.join(path_blue, f))])
    count_red = len([f for f in os.listdir(path_red) if os.path.isfile(os.path.join(path_red, f))])
    if not os.path.exists(path_blue): os.mkdir(path_blue)
    if not os.path.exists(path_red): os.mkdir(path_red)
    '''
    img.save(dest)

pull_dest = './frames/macu_vs_uofa/fps'
save_dest = './dataset/sentry'
# Get all .jpg files
urls = [os.path.join(pull_dest, f) for f in os.listdir(pull_dest) if f.lower().endswith('.jpg')]
f = open(save_dest + "annotation.txt", "w")
for url in urls:
    img, w, h = open_img(url)
    pts = get_annotation(img)
    acc_x, acc_y = compute_pixel_coords(pts, w, h)
    save = user_verify(img, acc_x, acc_y)
    if not save: continue # Ignore if not verified by the user
    save_with_labels(img, acc_x, acc_y, save_dest)
    for pt in pts:
        f.write(f"{url.split('/')[-1]},{pt['x']},{pt['y']},{acc_x},{acc_y}")
f.close()

