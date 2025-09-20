import os.path

from resolve_tools.resolve_utils import ResolveUtils
from proj_tools.proj_utils import ProjectUtils
from proj_tools.proj_naming import NamingConvention
from proj_tools.proj_data import Config



class ShotIdentifier:
    def __init__(self):
        self.resolve_utils = ResolveUtils()
        self.proj_utils = ProjectUtils()
        self.naming = NamingConvention().naming
        self.config = Config().get_config()

    def shots_ids(self, mode, clip_color, marker_color, seq, index_offset, dry_run=True, curr=False):
        if mode == 'Versions':
            self._as_versions(clip_color, seq, index_offset, dry_run)
        elif mode == 'Markers':
            self._as_markers(clip_color, marker_color, seq, index_offset, dry_run)
        elif mode == "Clip Name":
            self._as_clipname(clip_color, marker_color, seq, index_offset, dry_run)
            # self.proj_utils.message("Feature not implemented... yet")

    def _as_markers(self, clip_color, marker_color, seq, index_offset, dry_run=True, curr=False):
        clips_dict = self.resolve_utils.get_clips(clip_color, seq, index_offset)
        for clip_id, clip_data in clips_dict.items():
            custom_data = ["marker_type: vfx"]
            clip = clip_data['clip']
            shot_id = clip_data['shot_id']

            # Openclip
            openclip_name = self.naming("image", "openclip", {"<shotid>": shot_id})
            openclip_path = self.naming("paths",
                                        "openclips",
                                        {
                                             "<proj_root>": self.config['project']['path'],
                                             "<proj>": self.config['project']['alias'],
                                             "<seq>": seq
                                         }
                                        )
            # openclip_name = openclip_info["name"]
            # openclip_path = openclip_info["path"]
            # print(openclip_path)
            openclip = os.path.join(openclip_path, openclip_name["name"])
            # print(openclip)
            custom_data.append(f"openclip: {openclip}")

            # Add Marker
            clip_dur = clip_data['clip_dur']
            marker_frame = clip_data['clip_vfx_marker']

            for k, v in clip_data.items():
                custom_data.append(f"{k}: {v}")
            marker_custom_data = '\n'.join(custom_data)
            message_custom_data = '\n  '.join(custom_data)
            if not dry_run:
                clip.DeleteMarkersByColor(marker_color)
                marker = clip.AddMarker(
                    marker_frame,
                    marker_color,
                    shot_id,
                    "VFX Shot",
                    clip_dur - 1,
                    marker_custom_data
                )
                if marker:
                    self.proj_utils.message(f"Added marker at FrameId: {marker_frame + 1}")

            self.proj_utils.message('\n-------------------------------------')
            self.proj_utils.message(f"||||| Shot: {shot_id}")
            self.proj_utils.message('-------------------------------------')
            self.proj_utils.message(f"Added marker at FrameId: {marker_frame + 1}")
            self.proj_utils.message("Marker Custom Data:")
            self.proj_utils.message(message_custom_data)

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

    def _as_clipname(self, clip_color, marker_color, seq, index_offset, dry_run=True, curr=False):
        # Need Resolve 20.2+
        resolve_version = self.resolve_utils.get_resolve_version()
        self.proj_utils.message(resolve_version)

        if "20.2" not in resolve_version:
            self.proj_utils.message("This feature requires DaVinci Resolve 20.2 or higher.")
            return

        clips_dict = self.resolve_utils.get_clips(clip_color, seq, index_offset)
        for clip_id, clip_data in clips_dict.items():
            custom_data = ["marker_type: vfx"]
            clip = clip_data['clip']
            shot_id = clip_data['shot_id']

            # Openclip
            # openclip_name = self.naming("image", "openclip", {"<shotid>": shot_id})
            # openclip_path = self.naming("paths",
            #                             "openclips",
            #                             {
            #                                 "<proj_root>": self.config['project']['path'],
            #                                 "<proj>": self.config['project']['alias'],
            #                                 "<seq>": seq
            #                             }
            #                             )
            # openclip_name = openclip_info["name"]
            # openclip_path = openclip_info["path"]
            # print(openclip_path)
            # openclip = os.path.join(openclip_path, openclip_name["name"])
            # print(openclip)
            # custom_data.append(f"openclip: {openclip}")

            # Add Marker
            clip_dur = clip_data['clip_dur']
            marker_frame = clip_data['clip_vfx_marker']

            for k, v in clip_data.items():
                custom_data.append(f"{k}: {v}")
            marker_custom_data = '\n'.join(custom_data)
            message_custom_data = '\n  '.join(custom_data)
            if not dry_run:
                clip.DeleteMarkersByColor(marker_color)
                marker = clip.AddMarker(
                    marker_frame,
                    marker_color,
                    shot_id,
                    "VFX Shot",
                    clip_dur - 1,
                    marker_custom_data
                )
                if marker:
                    self.proj_utils.message(f"Added marker at FrameId: {marker_frame + 1}")

                shot_name = clip.SetName(shot_id)
                if shot_name:
                    self.proj_utils.message(f"Added Shot: {shot_id}")

            self.proj_utils.message('\n-------------------------------------')
            self.proj_utils.message(f"||||| Shot: {shot_id}")
            self.proj_utils.message('-------------------------------------')
            self.proj_utils.message(f"Added marker at FrameId: {marker_frame + 1}")
            self.proj_utils.message("Marker Custom Data:")
            self.proj_utils.message(message_custom_data)

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
            elif mode == 'Clip Name':
                if not dry_run:
                    clip.DeleteMarkersByColor(flag_color)
                    clip.SetName(clip_data['media_clip'])
                    self.proj_utils.message(f"\ndeleted Clip Name IDS: {clip_data['shot_id']}")


if __name__ == "__main__":
    shot_identifier = ShotIdentifier()
    # Example usage:
    # shot_identifier.shots_ids('Markers', 'Blue', 'Red', 'SEQ01', 10)
    # shot_identifier.clear_ids('Blue', 'Red', 'SEQ01', 'Markers')