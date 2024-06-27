from abc import ABC, abstractmethod


class IReplicateGenerator(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_replicate_response(self, prompt: str, num_outputs: int, guidance_scale: int, num_inference_steps: int) -> str:
        pass