# from transformers import TrOCRProcessor, VisionEncoderDecoderModel
# from PIL import Image
#
# # load image from the IAM database
# url = '/home/trootech/Documents/img.jpg'
# image = Image.open(url).convert("RGB")
#
# # Load model directly
# from transformers import AutoTokenizer, AutoModelForImageTextToText
#
# tokenizer = AutoTokenizer.from_pretrained("microsoft/trocr-small-handwritten")
# model = AutoModelForImageTextToText.from_pretrained("microsoft/trocr-small-handwritten")
#
# processor = TrOCRProcessor.from_pretrained('/home/trootech/workspace/transformers/trocr-small-handwritten')
# # model = VisionEncoderDecoderModel.from_pretrained('/home/trootech/workspace/transformers/trocr-small-handwritten')
# pixel_values = processor(images=image, return_tensors="pt").pixel_values
#
# generated_ids = model.generate(pixel_values)
# generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
#
#
# print('\n\n generated_text-->>', generated_text)
# from transformers import AutoTokenizer, AutoModelForImageTextToText
# from PIL import Image
# import torch
# from torchvision import transforms
#
# # Load image
# url = '/home/trootech/Documents/img.jpg'
# image = Image.open(url).convert("RGB")
#
# # Image preprocessing (manually handling the image transformation)
# transform = transforms.Compose([
#     transforms.Resize((32, 128)),  # Resize to model's expected input size
#     transforms.ToTensor(),         # Convert to tensor
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize
# ])
#
# image_tensor = transform(image).unsqueeze(0)  # Add batch dimension
#
# # Load model and tokenizer
# tokenizer = AutoTokenizer.from_pretrained("microsoft/trocr-small-handwritten")
# model = AutoModelForImageTextToText.from_pretrained("microsoft/trocr-small-handwritten")
#
# # Use the model to generate text
# with torch.no_grad():  # No need to compute gradients
#     generated_ids = model.generate(image_tensor)
#
# # Decode the generated tokens
# generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
#
# print('\n\nGenerated Text:', generated_text)
#



