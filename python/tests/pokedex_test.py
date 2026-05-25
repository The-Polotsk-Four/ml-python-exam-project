import numpy as np
import sys
import os
import importlib.util # Bruges til at load vores predic model fil

module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "streamlit", "functions", "model_predict.py")

spec = importlib.util.spec_from_file_location("model_predict", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
# Vi finder vores model i filerne og
# loader den derefter med det udvalgte bibleotek
# Så vi kan bruge den i vores test


predict_pokemon = module.predict_pokemon

TEST_IMAGE = "/Users/gustavwilquin/Desktop/KEA Filer/4. Semester/Eksamen/ml-python-exam-project/machine_learning/roboflow_model/Pokemon-1/test/Eevee/00d762c891aa45b38173ce8bf9e74a4d_jpg.rf.69fc4a87cd57deabe307ea6f6d8b606b.jpg"
# Ruten til billedet som vi bruger i vores test

def test_pokemon_name_is_string():
    name, score, image = predict_pokemon(TEST_IMAGE)
    assert isinstance(name, str)
    # Tester om navnet er en string

def test_confidence_score_between_0_and_1():
    name, score, image = predict_pokemon(TEST_IMAGE)
    assert 0.0 <= score <= 1.0
    # Tjekker om scoren er mellem 0 og 1

def test_image_is_numpy_array():
    name, score, image = predict_pokemon(TEST_IMAGE)
    assert isinstance(image, np.ndarray)
    # Tester om billedet er i det rigtige format

def test_pokemon_name_is_not_empty():
    name, score, image = predict_pokemon(TEST_IMAGE)
    assert len(name) > 0
    # Tester om navnet er en tom streng

def test_confidence_score_is_not_zero():
    name, score, image = predict_pokemon(TEST_IMAGE)
    assert score > 0
    # Tester om modellen overhovedet er sikker

def test_image_has_three_color_channels():
    name, score, image = predict_pokemon(TEST_IMAGE)
    assert image.shape[2] == 3
    # Tester om billedet er RGB

def test_image_has_valid_dimensions():
    name, score, image = predict_pokemon(TEST_IMAGE)
    assert image.shape[0] > 0
    assert image.shape[1] > 0
    # Tester om billedet har en højde og bredde

def test_function_returns_exactly_three_values():
    result = predict_pokemon(TEST_IMAGE)
    assert len(result) == 3
    # Tester om funktionen faktisk returnere navn, score og billede