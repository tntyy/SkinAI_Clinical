import os
import uuid

import cv2
import numpy as np

from app.ai.gradcam import generate_gradcam
from app.ai.load_model import get_model

HEATMAP_DIR = "app/static/uploads/heatmap"
OVERLAY_DIR = "app/static/uploads/overlay"

os.makedirs(
    HEATMAP_DIR,
    exist_ok=True
)

os.makedirs(
    OVERLAY_DIR,
    exist_ok=True
)


def create_heatmap(image_path):

    model = get_model()

    heatmap = generate_gradcam(
        model,
        image_path
    )

    original = cv2.imread(image_path)

    if original is None:
        raise Exception("Không đọc được ảnh")

    heatmap = cv2.resize(
        heatmap,
        (
            original.shape[1],
            original.shape[0]
        )
    )

    heatmap = np.uint8(255 * heatmap)

    heatmap_color = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    overlay = cv2.addWeighted(
        original,
        0.6,
        heatmap_color,
        0.4,
        0
    )

    filename = f"{uuid.uuid4().hex}.jpg"

    heatmap_file = os.path.join(
        HEATMAP_DIR,
        filename
    )

    overlay_file = os.path.join(
        OVERLAY_DIR,
        filename
    )

    cv2.imwrite(
        heatmap_file,
        heatmap_color
    )

    cv2.imwrite(
        overlay_file,
        overlay
    )

    return (
        f"uploads/heatmap/{filename}",
        f"uploads/overlay/{filename}"
    )