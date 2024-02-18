from typing import Optional

import numpy as np
from loguru import logger

from osam import _models
from osam import types

model: Optional[_models.ModelBase] = None


def generate(request: types.GenerateRequest) -> types.GenerateResponse:
    global model

    model_cls = _models.get_model_class_by_name(name=request.model)
    if model is None or model.name != model_cls.name:
        model = model_cls()

    image: np.ndarray = request.image

    if request.prompt is None:
        height, width = image.shape[:2]
        prompt = types.Prompt(
            points=np.array([[width / 2, height / 2]], dtype=np.float32),
            point_labels=np.array([1], dtype=np.int32),
        )
        logger.warning(
            "Prompt is not given, so using the center point as prompt: {prompt!r}",
            prompt=prompt,
        )
    else:
        prompt = request.prompt

    image_embedding: types.ImageEmbedding = model.encode_image(image=image)
    mask: np.ndarray = model.generate_mask(
        image_embedding=image_embedding, prompt=prompt
    )
    return types.GenerateResponse(model=request.model, mask=mask)
