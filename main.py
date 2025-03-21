from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

# load image from the IAM database
url = '/home/trootech/Documents/img.jpg'
image = Image.open(url).convert("RGB")

processor = TrOCRProcessor.from_pretrained('/home/trootech/PycharmProjects/trocr-small-handwritten', use_fast=False)
model = VisionEncoderDecoderModel.from_pretrained('/home/trootech/PycharmProjects/trocr-small-handwritten')
pixel_values = processor(images=image, return_tensors="pt").pixel_values

generated_ids = model.generate(pixel_values)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]


print('\n\n generated_text-->>', generated_text)