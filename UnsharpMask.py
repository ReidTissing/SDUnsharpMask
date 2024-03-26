import modules.scripts as scripts
import gradio as gr
import os
from modules import images
from modules.processing import process_images, Processed
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state

class Script(scripts.Script):  

   def title(self):
     return "Unsharp Mask"

#only show in img2img tab

   def show(self, is_img2img):
     return is_img2img

#Gradio interface parameters 

   def ui(self, is_img2img):
     save = gr.Checkbox(False, label="Save original and effect")
     umradius = gr.Slider(minimum=0.0, maximum=1000.0, step=1, value=0, label="Radius")
     umpercent = gr.Slider(minimum=0.0, maximum=500.0, step=1, value=0, label="Percent")
     umthreshold = gr.Slider(minimum=0.0, maximum=255.0, step=1, value=0, label="Threshold")
     return [save, umradius, umpercent, umthreshold]

#processed object
   def run(self, p, save, umradius, umpercent, umthreshold):

#perform unsharp mask operation
     def unsharp_mask(im, umradius, umpercent, umthreshold):
       from PIL import Image, ImageFilter
       raf = im
       raf = raf.filter(filter=ImageFilter.UnsharpMask(radius = umradius, percent = umpercent, threshold = umthreshold))
       return raf

# If save is off, save with prefix filename
     basename = ""
     if(save):
       basename += "unsharpmask_"
     else:
       p.do_not_save_samples = True

#process images
     proc = process_images(p)

     for i in range(len(proc.images)):

       proc.images[i] = unsharp_mask(proc.images[i],  umradius, umpercent, umthreshold)
       images.save_image(proc.images[i], p.outpath_samples, basename,
       proc.seed + i, proc.prompt, opts.samples_format, info= proc.info, p=p)

     return proc
