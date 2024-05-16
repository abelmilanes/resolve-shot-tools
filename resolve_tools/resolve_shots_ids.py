#!/usr/bin/python3
from resolve_tools.resolve_utils import get_clips
from proj_tools.proj_utils import message


def shots_ids(mode, clip_color, marker_color, seq, index_offset, dry_run=True, curr=False):
    if mode == 'Versions':
        as_versions(clip_color, seq, index_offset, dry_run)
    elif mode == 'Markers':
        as_markers(clip_color, marker_color, seq, index_offset, dry_run)
    else:
        message("Feature not implemented in Resolve")
        pass


def as_markers(clip_color, marker_color, seq, index_offset, dry_run=True, curr=False):
    clips_dict = get_clips(clip_color, seq, index_offset)
    for clip_id, clip_data, in clips_dict.items():
        clip = clip_data['clip']
        shot_id = clip_data['shot_id']

        # Add Marker
        clip_dur = clip_data['clip_dur']
        marker_frame = clip_data['clip_vfx_marker']
        custom_data = ["marker_type: vfx"]
        for k, v in clip_data.items():
            custom_data.append("%s: %s" % (k, v))
        custom_data = '\n'.join(custom_data)
        if not dry_run:
            clip.DeleteMarkersByColor(marker_color)
            marker = clip.AddMarker(marker_frame, marker_color, shot_id, "VFX Shot", clip_dur - 1, custom_data)
            if marker:
                message("Added marker at FrameId: " + str(marker_frame + 1))
        message('\n-------------------------------------')
        message("||||| Shot: " + shot_id)
        message('-------------------------------------')
        message("Added marker at FrameId: " + str(marker_frame + 1))
        message(custom_data)


def as_versions(clip_color, seq, index_offset, dry_run=True):
    clips_dict = get_clips(clip_color, seq, index_offset)
    for clip_id, clip_data in clips_dict.items():
        clip = clip_data['clip']
        shot_id = clip_data['shot_id']
        message('-------------------------------------')
        message("%s - %s" % (clip_data['media_clip'], shot_id))
        message("Timecode IN: %s" % (clip_data['clip_timecode_in']))
        try:
            mk_versions = ['neutral', shot_id]
            for mk_version in mk_versions:
                try:
                    clip.LoadVersionByName(shot_id)
                    if mk_version not in clip.GetVersionNameList(0):
                        if not dry_run:
                            clip.AddVersion(mk_version, 0)
                        # print("added: "+mkv)
                        message("added: "+mk_version)
                    else:
                        message(mk_version)
                except Exception as err:
                    print(err)
                    pass

            for ver in clip.GetVersionNameList(0):
                if ver not in mk_versions:
                    if not dry_run:
                        clip.DeleteVersionByName(ver, 0)
                    message("deleted: "+ver)
            clip.LoadVersionByName(shot_id)
        except Exception as del_ex:
            print(del_ex)
            pass

    return


def clear_ids(clip_color, flag_color, seq, mode, dry_run=True):
    clips_dict = get_clips(clip_color, seq, 0)
    for clip_id, clip_data in clips_dict.items():
        clip = clip_data['clip']
        if mode == 'Markers':
            if not dry_run:
                clip.DeleteMarkersByColor(flag_color)
                message("\ndeleted Marker IDS: " + clip_data['shot_id'])
        elif mode == 'Versions':
            if not dry_run:
                for ver in clip.GetVersionNameList(0):
                    clip.DeleteVersionByName(ver, 0)
                    message("\ndeleted: " + ver)


if __name__ == "__main__":
    pass
