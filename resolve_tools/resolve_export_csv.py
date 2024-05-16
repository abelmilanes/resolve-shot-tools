import csv

from proj_tools.proj_data import config as proj_config
from resolve_tools.resolve_utils import get_clips


def export_csv(seq, clip_color, dryrun=True):
    config = proj_config()
    project = config['project']['name']
    data_dict = []
    clips_data = get_clips(clip_color, seq)
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
