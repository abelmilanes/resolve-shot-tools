import csv

from proj_tools.proj_data import Config
from resolve_tools.resolve_utils import ResolveUtils


def export_csv(seq, clip_color, index_offset, dryrun=True):
    resolve_utils = ResolveUtils()
    config = Config().get_config()

    project = config['project']['name']
    data_dict = []
    get_clips = resolve_utils.get_clips
    clips_data = get_clips(clip_color, seq, index_offset)
    for clip, data in clips_data.items():
        csv_dict = {'Project': project,
                    'Episode': '',
                    'Sequence': seq,
                    'Name': data['shot_id'],
                    'Description': data['clip_name'],
                    'Nb Frames': int(data['out']) - int(data['in']),
                    'FPS': '24',
                    'Frame In': data['in'],
                    'Frame Out': data['out'],
                    'Focal': data['focal'],
                    'FStop': data['fstop']
                    }
        data_dict.append(csv_dict)

    csv_columns = ['Project',
                   'Episode',
                   'Sequence',
                   'Name',
                   'Description',
                   'Nb Frames',
                   'FPS',
                   'Frame In',
                   'Frame Out',
                   'Artist',
                   'Status',
                   'Notes',
                   'Focal',
                   'FStop']

    csv_dir = config['kitsu']['config_folder']
    csv_file = "%s/%s_kitsu_shots.csv" % (csv_dir, seq)
    print(csv_file)
    if not dryrun:
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in data_dict:
                    writer.writerow(d)
                print(csv_file)
        except IOError as e:
            print("I/O error:", e)
    print(data_dict)


if __name__ == "__main__":
    pass
