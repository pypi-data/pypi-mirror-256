from PIL import ImageDraw
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch
from transformers import Pix2StructProcessor, Pix2StructVisionModel
from askui_ml_helper.utils.image import download_default_font, render_header

class Pix2StructForRegression(nn.Module):
    def __init__(self, sourcemodel_path, device):
        super(Pix2StructForRegression, self).__init__()
        self.model = Pix2StructVisionModel.from_pretrained(sourcemodel_path)
        self.regression_layer1 = nn.Linear(768, 1536)
        self.dropout1 = nn.Dropout(0.1)
        self.regression_layer2 = nn.Linear(1536, 768)
        self.dropout2 = nn.Dropout(0.1)
        self.regression_layer3 = nn.Linear(768, 2)
        self.device = device

    def forward(self, *args, **kwargs):
        outputs = self.model(*args, **kwargs)
        sequence_output = outputs.last_hidden_state
        first_token_output = sequence_output[:, 0, :]

        x = F.relu(self.regression_layer1(first_token_output))
        x = F.relu(self.regression_layer2(x))
        regression_output = torch.sigmoid(self.regression_layer3(x))

        return regression_output

    def load_state_dict_file(self, checkpoint_path, strict=True):
        state_dict = torch.load(checkpoint_path, map_location=self.device)
        self.load_state_dict(state_dict, strict=strict)

class PtaTextInference:
    def __init__(self, local_checkpoint_path) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.processor = self.load_model_and_processor("google/matcha-base", local_checkpoint_path)

    def load_model_and_processor(self, model_name, checkpoint_path):
        model = Pix2StructForRegression(sourcemodel_path=model_name, device=self.device)
        model.load_state_dict_file(checkpoint_path=checkpoint_path)
        model.eval()
        model = model.to(self.device)
        processor = Pix2StructProcessor.from_pretrained(model_name, is_vqa=False)
        return model, processor

    def prepare_image(self, image, prompt, processor):
        image = image.resize((1920, 1080)) # manual for pta-text-v0.1.pt
        download_default_font_path = download_default_font()
        rendered_image, _, render_variables = render_header(
            image=image,
            header=prompt,
            bbox={"xmin": 0, "ymin": 0, "xmax": 0, "ymax": 0},
            font_path=download_default_font_path,
        )
        encoding = processor(
            images=rendered_image,
            max_patches=2048, # manual for pta-text-v0.1.pt
            add_special_tokens=True,
            return_tensors="pt",
        )
        return encoding, render_variables

    def predict_coordinates(self, encoding, model, render_variables):
        with torch.no_grad():
            pred_regression_outs = model(flattened_patches=encoding["flattened_patches"], attention_mask=encoding["attention_mask"])
            new_height = render_variables["height"]
            new_header_height = render_variables["header_height"]
            new_total_height = render_variables["total_height"]

            pred_regression_outs[:, 1] = (
                (pred_regression_outs[:, 1] * new_total_height) - new_header_height
            ) / new_height

            pred_coordinates = pred_regression_outs.squeeze().tolist()
        return pred_coordinates

    def draw_circle_on_image(self, image, coordinates, radius = 5):
        x, y = coordinates[0] * image.width, coordinates[1] * image.height
        draw = ImageDraw.Draw(image)
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill="red")
        return image

    def process_image(self, image, prompt):
        encoding, render_variables = self.prepare_image(image, prompt, self.processor)
        pred_coordinates = self.predict_coordinates(encoding.to(self.device) , self.model, render_variables)
        return pred_coordinates

    def process_image_and_draw_circle(self, image, prompt, radius = 5):
        pred_coordinates = self.process_image(image, prompt)
        result_image = self.draw_circle_on_image(image, pred_coordinates, radius=radius)
        return result_image
