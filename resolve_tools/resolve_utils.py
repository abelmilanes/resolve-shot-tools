import sys
from proj_tools.proj_utils import message
from resolve_tools.resolve_connect import current_timeline, current_project
from utils.timecode import frames_to_timecode
from proj_tools.proj_data import config
from proj_tools.proj_naming import naming


def get_timeline_clips():
    try:
        timeline_clips = None
        ct_track_name = config()['resolve']['vfx_plate_trk_name']
        tracks = range(current_timeline().GetTrackCount('video'))
        if len(tracks) == 1:
            tracks = [1]
        for index in tracks:
            track_name = current_timeline().GetTrackName('video', index)
            if track_name == ct_track_name:
                print(f"Using Video Track: {ct_track_name}")
                # message("Generating shots from video track: "+track_name)
                timeline_clips = current_timeline().GetItemListInTrack('video', index)
        return timeline_clips
    except Exception as ex:
        print("Error: ", ex)
        sys.exit()
        pass


def get_clips(clip_color, seq, offset_index):
    all_clips_dict = {}
    shot_interval = config()['kitsu']['shot_interval']
    first_index = None
    timeline_clips = get_timeline_clips()
    try:
        first_index = next(timeline_clips.index(clip) for clip in timeline_clips if clip_color == clip.GetClipColor())
    except StopIteration:
        print("No clip with the specified color found.")
        raise
    first_index = first_index * int(shot_interval) + int(shot_interval)
    for clip in timeline_clips:
        # print(clip)
        cur_color = clip.GetClipColor()
        clip_dict = {}
        if clip_color == cur_color:
            clip_index = timeline_clips.index(clip)
            clip_index_int = int(clip_index) * int(shot_interval) + int(shot_interval)
            if offset_index:
                clip_index_int = (clip_index_int-first_index)+int(offset_index)
            shot_id = naming('shotid', "name", {"seq": seq, "id": clip_index_int})

            # Get shot_id from marker
            try:
                clip_markers = clip.GetMarkers()
                for marker in clip_markers:
                    marker_custom_data = clip.GetMarkerCustomData(marker)
                    # message(marker_custom_data)
                    if "marker_type: vfx" in marker_custom_data:
                        marker_name = clip_markers[marker]["name"]
                        message(marker_name)
                        if not marker_name == shot_id:
                            # Account for custom shot name
                            shot_id = marker_name
            except Exception as e:
                print("Error: ", e)
                pass
            clip_unique_id = clip.GetUniqueId()
            clip_dict['unique_id'] = clip_unique_id
            clip_dict['color'] = cur_color
            clip_dict['clip_index'] = clip_index
            clip_dict['clip_name'] = clip.GetName()
            clip_dict['clip_start'] = clip.GetStart()
            clip_dict['clip_timecode_in'] = frames_to_timecode(clip.GetStart(), 23.976, False)
            clip_dict['clip_end'] = clip.GetEnd()
            clip_dict['clip_timecode_out'] = frames_to_timecode(clip.GetEnd(), 23.976, False)
            clip_dict['clip_vfx_marker'] = clip.GetLeftOffset()
            clip_dict['clip_dur'] = clip.GetDuration()
            clip_dict['shot_id'] = shot_id
            clip_dict['in'] = 1001
            clip_dict['out'] = 1000 + int(clip.GetDuration() + 16)
            clip_dict['cut_in'] = 1009
            clip_dict['cut_out'] = 1000 + int(clip.GetDuration() + 8)
            media_item = clip.GetMediaPoolItem()
            clip_dict['media_clip'] = media_item.GetName()
            clip_dict['focal'] = media_item.GetMetadata('Focal Point (mm)')
            clip_dict['fstop'] = media_item.GetMetadata('Camera Aperture')
            clip_dict['resolve_project'] = current_project().GetName()
            clip_dict['resolve_timeline'] = current_timeline().GetName()
            clip_dict['resolve_clip_color'] = clip.GetClipColor()
            clip_dict['clip'] = clip
            all_clips_dict[clip_unique_id] = clip_dict

    return all_clips_dict


def render_odt(odt):
    curr_time = current_timeline().GetCurrentTimecode()
    print(curr_time)
    message('Setting ODT: '+odt)
    current_project().SetSetting('colorAcesODT', odt)


def render_presets():
    rndr_presets = current_project().GetRenderPresets()
    return rndr_presets


def go_to_frame(frame, go=False):
    frame_rate = float(current_timeline().GetSetting("timelineFrameRate"))
    timecode = frames_to_timecode(frame, frame_rate, False)
    if go:
        current_timeline().SetCurrentTimecode(timecode)
    return timecode


if __name__ == "__main__":
    pass
