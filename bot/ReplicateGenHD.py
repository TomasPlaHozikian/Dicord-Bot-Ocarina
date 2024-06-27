import ReplicateGenerator
import replicate
from dotenv import load_dotenv
import os

#class that handles the replicate API to generate images based on str prompt
class ReplicateGenHD(ReplicateGenerator.IReplicateGenerator):
    #load env
    
    def __init__(self) -> None:
        load_dotenv()
        os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_KEY")
        self.model = "fofr/epicrealismxl-lightning-hades:0ca10b1fd361c1c5568720736411eaa89d9684415eb61fd36875b4d3c20f605a"
        
    
    def get_replicate_response(self, prompt: str, num_outputs: int, 
                               guidance_scale: int, num_inference_steps: int) -> str:
        input = {
            "prompt": prompt, 
            "num_outputs": num_outputs, 
            "guidance_scale": guidance_scale, 
            "num_inference_steps": num_inference_steps
        }
        return replicate.run(self.model, input)
        