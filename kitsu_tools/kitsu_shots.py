import gazu

from kitsu_tools.kitsu_thumbnail import get_thumb, post_preview
from resolve_tools.resolve_connect import resolve
from resolve_tools.resolve_utils import get_clips, go_to_frame
from proj_tools.proj_utils import message


def create_shot(config, proj, seq, clip_color, offset_index, dry_run=True):
    clips_dict = get_clips(clip_color, seq, offset_index)
    curr_page = resolve().GetCurrentPage()
    if not dry_run:
        resolve().OpenPage('color')
    for clip_id, clip_data in clips_dict.items():
        clip = clip_data["clip"]
        shot_id = clip_data['shot_id']

        # # Get shot_id from marker
        # try:
        #     clip_markers = clip.GetMarkers()
        #     for marker in clip_markers:
        #         marker_custom_data = clip.GetMarkerCustomData(marker)
        #         # message(marker_custom_data)
        #         if "marker_type: vfx" in marker_custom_data:
        #             marker_name = clip_markers[marker]["name"]
        #             message(marker_name)
        #             if not marker_name == shot_id:
        #                 # Account for custom shot name
        #                 shot_id = marker_name
        #                 clip_data['shot_id'] = marker_name
        # except Exception as e:
        #     print(e)
        #     pass

        ###################################
        # Check if shot is already in Kitsu
        project = gazu.project.get_project_by_name(proj)
        shots = gazu.shot.all_shots_for_project(project)
        shot_exist = False
        for s in shots:
            while s['name'] == shot_id:
                message('\nShot already in Kitsu: '+shot_id)
                shot_exist = True
                break
        ####################################

        if not shot_exist:
            message("-------------------------------------\nCreating Kitsu Shot for: "+proj)
            message("shot id: "+shot_id)
            message("in: "+str(clip_data['in']))
            message("out: "+str(clip_data['out']))
            kitsu_metadata = {
                'cut_in': clip_data['cut_in'],
                'cut_out': clip_data['cut_out'],
                'frames': clip_data['clip_dur'],
                'media': clip_data['media_clip'],
                'fps': '24',
                'lens': clip_data['focal'],
                'fstop': clip_data['fstop'],
                'notes': '',
                'tags': '',
                'resolve_info': {
                    'timecode in': clip_data['clip_timecode_in'],
                    'timecode out': clip_data['clip_timecode_out'],
                    'clip start': clip_data['clip_start'],
                    'clip end': clip_data['clip_end'],
                    'resolve project': clip_data['resolve_project'],
                    'resolve timeline': clip_data['resolve_timeline'],
                    'resolve clip color': clip_data['resolve_clip_color']
                }
            }
            for k, v in kitsu_metadata.items():
                message("%s: %s" % (k, v))

            if not dry_run:
                sequence = gazu.shot.get_sequence_by_name(project, seq, episode=None)
                if not sequence:
                    sequence = gazu.shot.new_sequence(project, seq, episode=None)
                get_descriptors = gazu.project.all_metadata_descriptors(project)
                descriptors = []
                for d in get_descriptors:
                    descriptors.append(d['name'])
                print(descriptors)
                # for metadata in kitsu_metadata:
                #     if metadata not in descriptors:
                #         print(dir(gazu.project.add_metadata_descriptor))
                #         gazu.project.add_metadata_descriptor(project, metadata, 'Shot')
                #         message('Created metadata descriptor: '+metadata)

                shot = gazu.shot.new_shot(
                    project,
                    sequence,
                    shot_id,
                    frame_in=clip_data['in'],
                    frame_out=clip_data['out'],
                    data=kitsu_metadata
                )

                go_to_frame(clip_data['clip_start']+1, True)
                preview = get_thumb(config, shot_id)
                ###########################################
                # shot_create_task: Compositing
                # shot_create_status: RTS  # Ready to start
                # shot_create_comment: Version 00
                task = config['kitsu']['shot_create_task']
                status = config['kitsu']['shot_create_status']
                comment = config['kitsu']['shot_create_comment']
                post_preview(preview, shot, task, status, comment, dry_run=False)
                ###########################################

    # Back to original Resolve Module
    if resolve().GetCurrentPage() != curr_page:
        resolve().OpenPage(curr_page)


if __name__ == "__main__":
    pass
