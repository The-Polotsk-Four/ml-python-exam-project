import pytest
import numpy as np
import sys
import os
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from streamlit.functions.model_predict import predict_pokemon
from torch._C import dtype
from ultralytics.models import yolo

@patch('streamlit.functions.model_predict.YOLO')
def test_returns_pokemon_name(mock_yolo):
    mock_prediction = MagicMock()
    mock_prediction.probs.top1 = 0
    mock_prediction.names = {0: 'pikachu'}
    mock_prediction.probs.top1conf.item.return_value = 0.95
    mock_prediction.plot.return_value = np.zeros((100, 100, 3), dtype=np.uint8)

    mock_yolo.return_value.predict.return_value = [mock_prediction]

    name, score, image = predict_pokemon('fake_pokemon.jpg')

    assert name == 'pikachu'

@patch("streamlit.functions.model_predict.YOLO")
def test_confidence_score_is_float(mock_yolo):
    mock_prediction = MagicMock()
    mock_prediction.probs.top1 = 0
    mock_prediction.names = {0: 'charmander'}
    mock_prediction.probs.top1conf.item.return_value = 0.87
    mock_prediction.plot.return_value = np.zeros((100, 100, 3), dtype=np.uint8)

    mock_yolo.return_value.predict.return_value = [mock_prediction]

    name, score, image = predict_pokemon("fake_image.jpg")

    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0

@patch("streamlit.functions.model_predict.YOLO")
def test_annotated_image_is_numpy_array(mock_yolo):
    mock_prediction = MagicMock()
    mock_prediction.probs.top1 = 0
    mock_prediction.names = {0: "bulbasaur"}
    mock_prediction.probs.top1conf.item.return_value = 0.76
    mock_prediction.plot.return_value = np.zeros((100, 100, 3), dtype=np.uint8)

    mock_yolo.return_value.predict.return_value = [mock_prediction]

    name, score, image = predict_pokemon("fake_image.jpg")

    assert isinstance(image, np.ndarray)