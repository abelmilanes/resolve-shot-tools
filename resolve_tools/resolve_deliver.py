import os
from resolve_tools.resolve_connect import ResolveConnection
from resolve_tools.resolve_utils import ResolveUtils
from proj_tools.proj_utils import ProjectUtils
from proj_tools.proj_naming import NamingConvention


def vfx_plate_job(config, clip_color, flag_color, seq, index_offset, job_preset, dry):
    naming = NamingConvention().naming
    resolve = ResolveConnection()
    resolve_utils = ResolveUtils()
    proj_utils = ProjectUtils()

    get_clips = resolve_utils.get_clips
    clips = get_clips(clip_color, seq, index_offset)

    for clip_id, clip_data in clips.items():
        clip = clip_data["clip"]
        flags = clip.GetFlags()
        shot_id = clip_data['shot_id']

        for k, v in flags.items():
            message = proj_utils.message
            message("\nCreating VFX Plate job for: "+shot_id)
            if v == flag_color:
                try:
                    current_project = resolve.get_current_project()
                    current_project.LoadRenderPreset(job_preset)
                    mark_in = clip.GetStart()
                    mark_out = int(clip.GetEnd())-1
                    project = config['project']['alias']

                    project_path = config['project']['path']
                    naming_data = naming('image', 'plate', {"<shotid>": shot_id, "<track_name>": "%{Track Name}"})
                    naming_path = naming_data['path']
                    naming_name = naming_data['name']
                    target_dir = os.path.join(project_path, project, seq, shot_id, naming_path, naming_name)
                    print(target_dir)
                    plate_name = naming_name+'.'
                    message(plate_name)
                    message(target_dir)
                    message("\n|||||||||||||||||||||||||||||||||\n")

                    render_settings = {
                        "MarkIn": mark_in,
                        "MarkOut": mark_out,
                        "TargetDir": target_dir,
                        "CustomName": plate_name
                    }
                    current_project.SetRenderSettings(render_settings)
                    if not dry:
                        current_project.AddRenderJob()
                except Exception as e:
                    print(e)
                    pass

    return


if __name__ == "__main__":
    pass
