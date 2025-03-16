from django.conf import settings
from .tf_classification import TFClassificationModel
from scans.models import OrganChoices

def get_ai_model(organ):
    if organ == OrganChoices.CHEST:
        model_path = settings.CHEST_MODEL_PATH
        labels = settings.CHEST_MODEL_LABELS
        return TFClassificationModel(model_path=model_path, target_size=(244, 244), labels=labels)
    else:
        raise ValueError("Invalid organ.")