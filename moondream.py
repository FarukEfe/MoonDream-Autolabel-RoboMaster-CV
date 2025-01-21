from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image

model_id = "vikhyatk/moondream2"
revision = "2024-08-26"  # Pin to specific version
model = AutoModelForCausalLM.from_pretrained(
    model_id, trust_remote_code=True, revision=revision
)
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

image = Image.open('./frames/macu_vs_uofa/fps/frame00660.jpg')
w, h = image.width, image.height
enc_image = model.encode_image(image)
print(w,h)
print(model.answer_question(enc_image, f"Return the center point (in pixel coordinates) of the number on the robot in the image, considerin that image width is {w} and image height is {h}.", tokenizer))