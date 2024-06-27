import ReplicateGenerator
import replicate
from dotenv import load_dotenv
import os

#class that handles the replicate API to generate images based on str prompt
class ReplicateGenAnime(ReplicateGenerator.IReplicateGenerator):
    def __init__(self) -> None:
        load_dotenv()
        os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_KEY")
        self.model = "cjwbw/anything-v4.0:42a996d39a96aedc57b2e0aa8105dea39c9c89d9d266caf6bb4327a1c191b061"
    
    
    def get_replicate_response(self, prompt: str, num_outputs: int, 
                               guidance_scale: int, num_inference_steps: int) -> str:
        input = {
            "prompt": prompt,
            "scheduler": "DPMSolverMultistep", 
            "num_outputs": num_outputs, 
            "guidance_scale": guidance_scale, 
            "num_inference_steps": num_inference_steps
        }
        return replicate.run(self.model, input)