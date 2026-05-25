import os
from ultralytics import YOLO


def predict_pokemon(pokemon_image):
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "machine_learning", "roboflow_model", "trained_yolo26_model", "weights", "best.pt")
    model = YOLO(model_path)

    prediction = model.predict(
        source=pokemon_image,
        imgsz=1280
    )

    predicted_pokemon = prediction[0]
    most_confident = predicted_pokemon.probs.top1
    most_confident_pokemon_name = predicted_pokemon.names[most_confident]
    highest_confidence_score = predicted_pokemon.probs.top1conf.item()
    annotated_image = predicted_pokemon.plot()

    return most_confident_pokemon_name, highest_confidence_score, annotated_image