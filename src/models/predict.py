"""
Module with Classifier class which contain 
Classifier.predict method for prediction Go Game Winner
by your image
"""

from torchvision import transforms, models
from typing import Optional, Tuple
import torch.nn as nn
import torch


class Classifier:
    def __init__(
        self,
        weights_url: Optional[str] = None,
        img_size: Optional[Tuple[int]] = (128, 128),
    ) -> None:
        """
        Args:
            weights_path:
                url to weights of the model
            img_size:
                size in which image would be resized as input for the model
        """
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        
        if weights_url is None:
            weights_url = "https://github.com/roykoand/GoWinnerPrediction/releases/download/version(-1)/DenseNet121_weights.h5"
        
        self.model = self._model_upload(weights_url)
        self.model.to(self.device)
        self.preprocess = transforms.Compose(
            [
                transforms.Resize(img_size),
                transforms.Grayscale(num_output_channels=3),
                transforms.ToTensor(),
            ]
        )

    def _model_upload(self, weights_url: str) -> models.densenet.DenseNet:
        """
        DenseNet121 model was the best at perfomance, so
        we will use it as the main model

        https://pytorch.org/hub/pytorch_vision_densenet/
        """
        model = torch.hub.load("pytorch/vision:v0.10.0", "densenet121")
        model.classifier = nn.Linear(1024, 2, bias=True)
        model.load_state_dict(
            torch.hub.load_state_dict_from_url(weights_url, progress=False, map_location=torch.device("cpu")))
        return model

    @torch.no_grad()
    def predict(self, image) -> str:
        probs = torch.sigmoid(self.model(torch.unsqueeze(self.preprocess(image), 0)))
        return "W" if torch.argmax(probs) == 1 else "B"
