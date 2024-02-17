import os
from dataclasses import dataclass
from typing import Any, Dict, Union

from flask import current_app


@dataclass
class ImageInfo:
    image_path: str
    image_ext: str
    data_path: str


def resolve_image_info(input_key: str, check_existing=True) -> Union[ImageInfo, None]:
    image_path = os.path.join(current_app.instance_path, input_key)

    if check_existing:
        # TODO: Also check if the file is really an image
        if not os.path.isfile(image_path):
            return None

    path_without_ext, ext = os.path.splitext(image_path)
    image_data_path = path_without_ext + '.json'
    return ImageInfo(
        image_path=image_path,
        image_ext=ext,
        data_path=image_data_path
    )
