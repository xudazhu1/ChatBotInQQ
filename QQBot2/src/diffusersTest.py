from unittest import result
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
torch.cuda.empty_cache()
# print(torch.cuda.memory_summary(device=None, abbreviated=False))

# model_id = "CompVis/stable-diffusion-v1-2"
model_id = "IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Anime-Chinese-v0.1"
# device = "cpu"


pipe = StableDiffusionPipeline.from_pretrained(model_id, use_auth_token=True)
# pipe = pipe.to(device)

prompt = "a photo of a robot that plays the piano"
ret = pipe(prompt)
print(ret)
image = ret.images[0]
image.save("m_result.png")
