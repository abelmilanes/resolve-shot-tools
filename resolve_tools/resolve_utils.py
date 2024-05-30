import sys
from proj_tools.proj_data import Config
from resolve_tools.resolve_connect import ResolveConnection
from utils.timecode import frames_to_timecode, adjust_timecode
from proj_tools.proj_naming import NamingConvention
from proj_tools.proj_utils import ProjectUtils


class ResolveUtils:
    def __init__(self):
        self.resolve = ResolveConnection()
        self.config = Config().get_config()
        self.frame_rate = float(self.resolve.get_current_timeline().GetSetting('timelineFrameRate'))

    def get_resolve_version(self):
        resolve = ResolveConnection().dr
        return f"{resolve.GetProductName()}: {resolve.GetVersionString()}"

    def get_timeline_clips(self):
        """Get clips from the configured video track in the current timeline."""
        try:
            timeline_clips = None
            ct_track_name = self.config['resolve']['vfx_plate_trk_name']
            tracks = range(self.resolve.get_current_timeline().GetTrackCount('video'))
            if len(tracks) == 1:
                tracks = [1]
            for index in tracks:
                track_name = self.resolve.get_current_timeline().GetTrackName('video', index)
                if track_name == ct_track_name:
                    print(f"Using Video Track: {ct_track_name}")
                    timeline_clips = self.resolve.get_current_timeline().GetItemListInTrack('video', index)
                    break
            return timeline_clips
        except Exception as ex:
            print("Error retrieving timeline clips:", ex)
            sys.exit(1)

    def get_clips(self, clip_color, seq, index_offset):
        naming = NamingConvention().naming
        """Get clips of a specific color and assign shot names based on their index in the timeline."""
        all_clips_dict = {}
        shot_interval = self.config['kitsu']['shot_interval']
        shot_start_frame = int(self.config['resolve']['vfx_shot_start_frame'])
        shot_handles = int(self.config['resolve']['vfx_shot_handles'])
        timeline_clips = self.get_timeline_clips()

        if not timeline_clips:
            print("No timeline clips found.")
            return all_clips_dict

        try:
            first_index = next(index for index, clip in enumerate(timeline_clips) if clip.GetClipColor() == clip_color)
        except StopIteration:
            print("No clip with the specified color found.")
            return all_clips_dict

        first_index = first_index * int(shot_interval) + int(shot_interval)
        for clip in timeline_clips:
            if clip.GetClipColor() == clip_color:
                clip_index = timeline_clips.index(clip)
                clip_index_int = clip_index * int(shot_interval) + int(shot_interval)
                if index_offset:
                    clip_index_int = (clip_index_int - first_index) + int(index_offset)
                shot_id = naming('shotid', "name", {"seq": seq, "id": clip_index_int})

                try:
                    clip_markers = clip.GetMarkers()
                    for marker in clip_markers:
                        marker_custom_data = clip.GetMarkerCustomData(marker)
                        if "marker_type: vfx" in marker_custom_data:
                            marker_name = clip_markers[marker]["name"]
                            if marker_name != shot_id:
                                shot_id = marker_name
                except Exception as e:
                    print("Error retrieving clip markers:", e)

                clip_dict = {
                    'unique_id': clip.GetUniqueId(),
                    'color': clip.GetClipColor(),
                    'clip_index': clip_index,
                    'clip_name': clip.GetName(),
                    'clip_start': clip.GetStart(),
                    'clip_timecode_in': frames_to_timecode(clip.GetStart(), self.frame_rate, False),
                    'clip_end': clip.GetEnd(),
                    'clip_timecode_out': frames_to_timecode(clip.GetEnd(), self.frame_rate, False),
                    'clip_vfx_marker': clip.GetLeftOffset(),
                    'clip_dur': clip.GetDuration(),
                    'shot_id': shot_id,
                    'in': shot_start_frame,
                    'out': (shot_start_frame - 1) + int(clip.GetDuration() + shot_handles * 2),
                    'cut_in': shot_start_frame + shot_handles,
                    'cut_out': (shot_start_frame - 1) + int(clip.GetDuration() + shot_handles),
                    'media_clip': clip.GetMediaPoolItem().GetName(),
                    'focal': clip.GetMediaPoolItem().GetMetadata('Focal Point (mm)'),
                    'fstop': clip.GetMediaPoolItem().GetMetadata('Camera Aperture'),
                    'resolve_project': self.resolve.get_current_project().GetName(),
                    'resolve_timeline': self.resolve.get_current_timeline().GetName(),
                    'resolve_clip_color': clip.GetClipColor(),
                    'clip': clip
                }
                all_clips_dict[clip.GetUniqueId()] = clip_dict

        return all_clips_dict

    def render_odt(self, odt):
        """Set the Output Device Transform (ODT) for the current project."""
        curr_timeline = self.resolve.get_current_timeline()
        curr_timecode = curr_timeline.GetCurrentTimecode()
        ProjectUtils().message(f'Setting ODT: {odt}')
        self.resolve.get_current_project().SetSetting('colorAcesODT', odt)
        temp_timecode = adjust_timecode(curr_timecode, 1, self.frame_rate)
        curr_timeline.SetCurrentTimecode(temp_timecode)
        curr_timeline.SetCurrentTimecode(curr_timecode)

    def render_presets(self):
        """Get available render presets for the current project."""
        return self.resolve.get_current_project().GetRenderPresets()

    def go_to_frame(self, frame, go=False):
        """Convert frame number to timecode and optionally set the current timeline timecode."""
        frame_rate = float(self.resolve.get_current_timeline().GetSetting("timelineFrameRate"))
        timecode = frames_to_timecode(frame, frame_rate, False)
        if go:
            self.resolve.get_current_timeline().SetCurrentTimecode(timecode)
        return timecode
