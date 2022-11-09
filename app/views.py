from django.shortcuts import render
from json import JSONDecoder
from django.views import View
from django.http import JsonResponse
from dotenv import load_dotenv
import torch
import warnings
import requests
import torch
import io
from PIL import Image
from io import BytesIO
import os
import json
import base64
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from diffusers import StableDiffusionImg2ImgPipeline, StableDiffusionPipeline
from django.views.decorators.csrf import csrf_exempt
import re

from backend.settings import BASE_DIR

load_dotenv(os.path.join(BASE_DIR, '.env'))

print(os.getenv("API_KEY"))

def test(request):
  return JsonResponse({"message": "Hello World"})

# def index(request):
#     return render(request, 'app/templates/index.html')

def index(request, template="index.html", ):
    return render(request, template, {})

def img2img_generate(request, page="generated_image.html", input_img = "imgs/distorted_head_before.jpg"):
# load the pipeline
  access_token = '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'
  device = "cuda" if torch.cuda.is_available() else "cpu"
  model_id_or_path = "CompVis/stable-diffusion-v1-4"
  pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    model_id_or_path,
    use_auth_token=True,
    cache_dir=os.getenv("cache_dir", "./models"),
  )
  pipe = pipe.to(device)

  init_image = Image.open(input_img)
  init_image = init_image.resize((768, 512))

  prompt = "fantasy landscape, trending on artstation"

  images = pipe(prompt=prompt, init_image=init_image, strength=0.50, guidance_scale=7.6).images

  print('hello world')

  return render(request, page, context={'image': images[0]})

def text2img_generate(request, page="generated_image.html"):
  print("recieved")
  pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")

# disable the following line if you run on CPU
#pipe = pipe.to("cuda")

  prompt = "a photo of an astronaut riding a horse on mars"
  images = pipe(prompt).images[0]  
  
  img = base64.b64encode(images)

  return JsonResponse({"img": img})


@csrf_exempt
def sdk_gen(request):
  body = json.loads(request.body)
  image_data = re.sub('^data:image/.+;base64,', '', body['start_img'])
  im = Image.open(BytesIO(base64.b64decode(image_data)))
  im = im.resize((768, 512))
  stability_api = client.StabilityInference(
    key= "sk-a6704AqvdMbtTfgtVDHHQ0NrrEpBvwnnBDOjQ9nTSNIQrg3m", 
    verbose=True,
  )

  answers = stability_api.generate(
    prompt= body["input"],
    seed= "", # if provided, specifying a random seed makes results deterministic
    steps=100, # defaults to 50 if not specified
    init_image= im
  )

# iterating over the generator produces the api response
  for resp in answers:
      for artifact in resp.artifacts:
          if artifact.finish_reason == generation.FILTER:
              return warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
          if artifact.type == generation.ARTIFACT_IMAGE:
              store = artifact.binary
              img = str(base64.b64encode(store))
              return JsonResponse({'img': img[2:-1]})