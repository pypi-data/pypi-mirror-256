import unittest
import subprocess
from PIL import Image
from askui_ml_helper.utils.pta_text import PtaTextInference # Update with the correct import path

class TestPtaTextInference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Download the checkpoint
        cls.checkpoint_path = "pta-text-v0.1.pt"
        subprocess.run([
            "curl", "-L", "https://huggingface.co/AskUI/pta-text-0.1/resolve/main/pta-text-v0.1.pt?download=true",
            "-o", cls.checkpoint_path
        ], check=True)

        # Initialize PtaTextInference with the downloaded checkpoint
        cls.pta_text_inference = PtaTextInference(cls.checkpoint_path)

    def test_process_image(self):
        # Create a dummy image
        dummy_image = Image.new('RGB', (1920, 1080), color='white')
        test_prompt = "Test Prompt"

        # Call process_image
        pred_coordinates = self.pta_text_inference.process_image(dummy_image, test_prompt)
        
        # Assertions can be added here based on expected pred_coordinates format
        self.assertIsInstance(pred_coordinates, list, "Predicted coordinates should be a list")
        self.assertEqual(len(pred_coordinates), 2, "Predicted coordinates should contain two elements")

    @classmethod
    def tearDownClass(cls):
        # Clean up downloaded files if necessary
        subprocess.run(["rm", cls.checkpoint_path], check=True)

if __name__ == "__main__":
    unittest.main()
