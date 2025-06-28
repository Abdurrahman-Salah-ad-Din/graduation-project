from django.conf import settings
from .tf_classification import TFClassificationModel
from .pytorch_classification import PytorchClassification
from .brain_pytorch_classification import BrainPyTorchClassification
from scans.models import OrganChoices
from .chest_ct_tf_classification import ChestCTTensorFlowClassification
from .bone_fracture_tf_classification import BoneFractureTensorFlowClassification
from .skin_tf_classification import SkinTensorFlowClassification

def get_ai_model(organ):
    if organ == OrganChoices.CHEST:
        model_path = settings.CHEST_MODEL_PATH
        labels = settings.CHEST_MODEL_LABELS
        target_size = settings.CHEST_MODEL_TARGET_SIZE
        return PytorchClassification(model_path=model_path, target_size=target_size, labels=labels)
    elif organ == OrganChoices.BRAIN:
        model_path = settings.BRAIN_MODEL_PATH
        labels = settings.BRAIN_MODEL_LABELS
        target_size = settings.BRAIN_MODEL_TARGET_SIZE
        return BrainPyTorchClassification(model_path=model_path, target_size=target_size, labels=labels)
    elif organ == OrganChoices.CHEST_CT:
        model_path = settings.CHEST_CT_MODEL_PATH
        labels = settings.CHEST_CT_MODEL_LABELS
        target_size = settings.CHEST_CT_MODEL_TARGET_SIZE
        return ChestCTTensorFlowClassification(model_path=model_path, target_size=target_size, labels=labels)
    elif organ == OrganChoices.BONE_FRACTURE:
        model_path = settings.BONE_FRACTURE_MODEL_PATH
        labels = settings.BONE_FRACTURE_MODEL_LABELS
        target_size = settings.BONE_FRACTURE_MODEL_TARGET_SIZE
        return BoneFractureTensorFlowClassification(model_path=model_path, target_size=target_size, labels=labels)
    elif organ == OrganChoices.SKIN:
        model_path = settings.SKIN_MODEL_PATH
        labels = settings.SKIN_MODEL_LABELS
        target_size = settings.SKIN_MODEL_TARGET_SIZE
        return SkinTensorFlowClassification(model_path=model_path, target_size=target_size, labels=labels)
    else:
        raise ValueError("Invalid organ.")