from resolve_tools.resolve_utils import ResolveUtils
from proj_tools.proj_utils import ProjectUtils


class ShotIdentifier:
    def __init__(self):
        self.resolve_utils = ResolveUtils()
        self.proj_utils = ProjectUtils()

    def shots_ids(self, mode, clip_color, marker_color, seq, index_offset, dry_run=True, curr=False):
        if mode == 'Versions':
            self._as_versions(clip_color, seq, index_offset, dry_run)
        elif mode == 'Markers':
            self._as_markers(clip_color, marker_color, seq, index_offset, dry_run)
        else:
            self.proj_utils.message("Feature not implemented... yet")

    def _as_markers(self, clip_color, marker_color, seq, index_offset, dry_run=True, curr=False):
        clips_dict = self.resolve_utils.get_clips(clip_color, seq, index_offset)
        for clip_id, clip_data in clips_dict.items():
            clip = clip_data['clip']
            shot_id = clip_data['shot_id']

            # Add Marker
            clip_dur = clip_data['clip_dur']
            marker_frame = clip_data['clip_vfx_marker']
            custom_data = ["marker_type: vfx"]
            for k, v in clip_data.items():
                custom_data.append(f"{k}: {v}")
            custom_data = '\n'.join(custom_data)

            if not dry_run:
                clip.DeleteMarkersByColor(marker_color)
                marker = clip.AddMarker(marker_frame, marker_color, shot_id, "VFX Shot", clip_dur - 1, custom_data)
                if marker:
                    self.proj_utils.message(f"Added marker at FrameId: {marker_frame + 1}")

            self.proj_utils.message('\n-------------------------------------')
            self.proj_utils.message(f"||||| Shot: {shot_id}")
            self.proj_utils.message('-------------------------------------')
            self.proj_utils.message(f"Added marker at FrameId: {marker_frame + 1}")
            self.proj_utils.message(custom_data)

    def _as_versions(self, clip_color, seq, index_offset, dry_run=True):
        clips_dict = self.resolve_utils.get_clips(clip_color, seq, index_offset)
        for clip_id, clip_data in clips_dict.items():
            clip = clip_data['clip']
            shot_id = clip_data['shot_id']
            self.proj_utils.message('-------------------------------------')
            self.proj_utils.message(f"{clip_data['media_clip']} - {shot_id}")
            self.proj_utils.message(f"Timecode IN: {clip_data['clip_timecode_in']}")

            try:
                mk_versions = ['neutral', shot_id]
                for mk_version in mk_versions:
                    try:
                        clip.LoadVersionByName(shot_id)
                        if mk_version not in clip.GetVersionNameList(0):
                            if not dry_run:
                                clip.AddVersion(mk_version, 0)
                            self.proj_utils.message(f"added: {mk_version}")
                        else:
                            self.proj_utils.message(mk_version)
                    except Exception as err:
                        print(err)

                for ver in clip.GetVersionNameList(0):
                    if ver not in mk_versions:
                        if not dry_run:
                            clip.DeleteVersionByName(ver, 0)
                        self.proj_utils.message(f"deleted: {ver}")
                clip.LoadVersionByName(shot_id)
            except Exception as del_ex:
                print(del_ex)

    def clear_ids(self, clip_color, flag_color, seq, mode, dry_run=True):
        clips_dict = self.resolve_utils.get_clips(clip_color, seq, 0)
        for clip_id, clip_data in clips_dict.items():
            clip = clip_data['clip']
            if mode == 'Markers':
                if not dry_run:
                    clip.DeleteMarkersByColor(flag_color)
                    self.proj_utils.message(f"\ndeleted Marker IDS: {clip_data['shot_id']}")
            elif mode == 'Versions':
                if not dry_run:
                    for ver in clip.GetVersionNameList(0):
                        clip.DeleteVersionByName(ver, 0)
                        self.proj_utils.message(f"\ndeleted: {ver}")


if __name__ == "__main__":
    shot_identifier = ShotIdentifier()
    # Example usage:
    # shot_identifier.shots_ids('Markers', 'Blue', 'Red', 'SEQ01', 10)
    # shot_identifier.clear_ids('Blue', 'Red', 'SEQ01', 'Markers')
