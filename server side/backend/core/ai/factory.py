from django.conf import settings
from .tf_classification import TFClassificationModel
from scans.models import OrganChoices

def get_ai_model(organ):
    if organ == OrganChoices.CHEST:
        model_path = settings.CHEST_MODEL_PATH
        labels = settings.CHEST_MODEL_LABELS
        target_size = settings.CHEST_MODEL_TARGET_SIZE
        return TFClassificationModel(model_path=model_path, target_size=target_size, labels=labels)
    else:
        raise ValueError("Invalid organ.")