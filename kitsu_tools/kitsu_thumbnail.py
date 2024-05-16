import base64
import os

import gazu
import numpy as np
from PIL import Image

from resolve_tools.resolve_connect import current_timeline


# Decode from base64 image string and return cv2 matrix image in BGR format for display
def readb64(base64_string, width, height):
    nparr = np.frombuffer(base64.b64decode(base64_string), np.uint8)
    nparr = nparr.reshape(int(height), int(width), 3)
    return Image.frombuffer('RGB', (width, height), nparr)


def get_thumb(config, shot_id):
    ct = current_timeline()
    project_name = config['project']['alias']
    project_dir = config['project']['path']
    config_folder = config['kitsu']['config_folder']
    thumbnail_dir = config['kitsu']['thumbnail_folder']
    thumbnail_name = "%s_%s.jpg" % (shot_id.split('_')[0], shot_id)
    thumbnail_path = os.path.join(project_dir, project_name, config_folder, "kitsu", thumbnail_dir)
    os.makedirs(thumbnail_path, exist_ok=True)
    filename = os.path.join(thumbnail_path, thumbnail_name)
    print(filename)

    curr_thumb = ct.GetCurrentClipThumbnailImage()
    print(dir(curr_thumb))
    if (curr_thumb is None) or (len(curr_thumb) == 0):
        print("There is no current media thumbnail")

    width = curr_thumb["width"]
    height = curr_thumb["height"]
    iformat = curr_thumb["format"]  # Currently we only have RBG 8 bit format

    print("Width of the thumbnail is " + str(width) + ", Height is " + str(height) + ", Format is " + str(iformat))

    imgstring = curr_thumb["data"]
    img = readb64(imgstring, width, height)
    img.save(filename, 'jpeg')

    return filename


def post_preview(preview_file, shot, task, stat, note, dry_run=True, del_file=False):
    task_type = gazu.task.get_task_type_by_name(task)
    # print(task_type)
    task_stat = gazu.task.get_task_status_by_short_name(stat)
    try:
        gazu.task.new_task(shot, task_type)
        print("Creating task: " + task)
    except Exception as e:
        print(e)
        pass
    task_sb = gazu.task.get_task_by_name(shot, task_type)
    # print(dir(gazu.task))
    comment = gazu.task.add_comment(task_sb, task_stat, note)

    preview_file = gazu.task.add_preview(
        task_sb,
        comment,
        preview_file
    )
    gazu.task.set_main_preview(preview_file)


if __name__ == "__main__":
    pass
