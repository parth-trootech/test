# Load model directly
from transformers import AutoProcessor, AutoModelForImageTextToText

processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-3B-Instruct")
model = AutoModelForImageTextToText.from_pretrained("Qwen/Qwen2.5-VL-3B-Instruct")


# from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

# load image from the IAM database
url = '/home/trootech/Documents/img.jpg'
image = Image.open(url).convert("RGB")

# processor = TrOCRProcessor.from_pretrained('/home/trootech/workspace/transformers/trocr-small-handwritten')
# model = VisionEncoderDecoderModel.from_pretrained('/home/trootech/workspace/transformers/trocr-small-handwritten')
pixel_values = processor(images=image, return_tensors="pt").pixel_values

generated_ids = model.generate(pixel_values)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]


print('\n\n generated_text-->>', generated_text)