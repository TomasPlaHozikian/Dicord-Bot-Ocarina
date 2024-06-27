import ReplicateGenerator
import replicate
from dotenv import load_dotenv
import os

#class that handles the replicate API to generate images based on str prompt
class ReplicateGenPortrait(ReplicateGenerator.IReplicateGenerator):
    #load env
    
    def __init__(self) -> None:
        load_dotenv()
        os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_KEY")
        self.model = "cjwbw/portraitplus:629a9fe82c7979c1dab323aedac2c03adaae2e1aecf6be278a51fde0245e20a4"
    
    def get_replicate_response(self, prompt: str) -> str:
        input = {
            "width": 768,
            "height": 768,
            "prompt": prompt, 
            "scheduler": "K_EULER_ANCESTRAL",
            "num_outputs": 1, 
            "guidance_scale": 7.5,
            "negative_prompt": "blender illustration hdr painted, multiple people",
            "num_inference_steps": 50
        }
        return replicate.run(self.model, input)