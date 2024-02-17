import json
import os
import shutil
from typing import Dict

from flask import Blueprint, request, abort, jsonify, current_app, send_file
from labeling.notebook import utils

bp = Blueprint("files", __name__, url_prefix="/api/files")


@bp.route("")
def list_files():
    input_path = _resolve_input_key(request.args.get('path', ''))
    listing_path = input_path['path']

    if not os.path.isdir(listing_path):
        return abort(404, "Directory not found")

    output = []
    for path, subdirs, files in os.walk(listing_path):

        if path == listing_path:
            relative_path = ''
        else:
            relative_path = os.path.relpath(path, listing_path)
            if any([dirname.startswith('.') for dirname in relative_path.split('/')]):
                continue

            output.append({'key': relative_path + '/'})

        for filename in files:
            file_path = os.path.join(path, filename)
            if os.path.isdir(file_path):
                continue

            name, ext = os.path.splitext(filename)
            if ext in ('.jpg', '.png', '.jpeg'):
                file_mtime = os.path.getmtime(file_path)
                file_size = os.path.getsize(file_path)
                output.append({
                    'key': os.path.join(relative_path, filename),
                    'size': file_size,
                    'modified': file_mtime * 1000
                })
                continue

    return jsonify(output)


@bp.route("/move", methods=("POST",))
def move():
    key_from = request.args.get('from', '')
    key_to = request.args.get('to', '')

    path_from = _resolve_input_key(key_from)['path']
    path_to = _resolve_input_key(key_to)['path']
    if not os.path.exists(path_from):
        return abort(404, f'Source file/directory "{path_from}" not found')

    if os.path.exists(path_to):
        return abort(400, f'Destination file/directory "{path_to}" already exists')

    if os.path.isdir(path_from):
        shutil.move(path_from, path_to)
        return jsonify({
            'message': f'Moved directory "{path_from}" to "{path_to}"'
        })
    else:
        image_info_from = utils.resolve_image_info(key_from)
        image_info_to = utils.resolve_image_info(key_to, check_existing=False)

        if not image_info_from:
            return abort(404, f'Source key "{key_from}" is not an image file.')

        if not image_info_to or image_info_to.image_ext != image_info_from.image_ext:
            return abort(400, f'Destination key "{key_to}" is not an compatible image file.')

        shutil.move(image_info_from.image_path, image_info_to.image_path)
        shutil.move(image_info_from.data_path, image_info_to.data_path)
        return jsonify({
            'message': f'Moved image and its data from "{key_from}" to "{key_to}"'
        })


@bp.route("/image/<path:key>", methods=("GET",))
def get_image(key):
    image_info = utils.resolve_image_info(key)
    if image_info is None:
        return abort(404, "Image not found")

    return send_file(image_info.image_path)


@bp.route("/image_data/<path:key>", methods=("GET",))
def get_image_data(key):
    image_info = utils.resolve_image_info(key)
    if image_info is None:
        return abort(404, "Image not found")

    if not os.path.isfile(image_info.data_path):
        return abort(404, "Image data not found")

    with open(image_info.data_path, 'r') as f:
        return json.load(f)


@bp.route("/image_data/<path:key>", methods=("PUT", "POST",))
def put_image_data(key):
    parsed_path = _resolve_input_key(key)

    data = request.get_json(force=True)
    data_path = parsed_path['path_without_ext'] + '.json'

    with open(data_path, 'w') as f:
        json.dump(data, f)

    return data


def _resolve_input_key(input_key: str) -> Dict[str, str]:
    # TODO: Not allow browsing outside the instance path
    path = os.path.join(current_app.instance_path, input_key)
    path_without_ext, ext = os.path.splitext(path)
    return {
        'path': path,
        'path_without_ext': path_without_ext,
        'ext': ext
    }
