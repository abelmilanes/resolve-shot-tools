#!.venv/bin/python

import os
import sys
import argparse

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

from ui import rst_ui as window


# Get Resolve render presets
def dr_render_presets():
    from resolve_tools.resolve_utils import render_presets
    presets = []
    for k, v in sorted(render_presets().items()):
        presets.append(v)
    return presets


def quit_app():
    # some actions to perform before actually quitting:
    print('CLEAN EXIT')
    QtWidgets.QApplication.quit()


class PrjApp(window.Ui_main_window, QtWidgets.QMainWindow):
    def __init__(self, project):
        super(PrjApp, self).__init__()
        from proj_tools.proj_data import project_config
        self.config = project_config(project)
        config = self.config
        self.render_presets = dr_render_presets()
        self.process = None
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.setWindowTitle('R.S.T')
        self.root_TE.setText(config['project']['path'])
        self.proj_TE.setText(config['project']['name'])
        self.seq_CB.addItems(config['project']['sequences'])
        self.clipcolor_CB.addItems(config['resolve']['clip colors'])
        self.flag_CB.addItems(config['resolve']['flag colors'])
        self.odt_CB.addItems(config['resolve']['odt'])
        self.createas_CB.addItems(config['resolve']['id_as'])
        self.createas_CB.setCurrentText('Markers')
        self.resolveshots_BT.clicked.connect(self.name_shots)
        self.renderjobs_BT.clicked.connect(lambda: self.render_jobs())
        self.job_presets_CB.addItems(self.render_presets)
        try:
            self.job_presets_CB.setCurrentText(config['resolve']['default_render_preset'])
        except Exception as e:
            print("vfx_plates preset not present", e)
        self.kitsushots_BT.clicked.connect(lambda: self.kitsu_create_shots())
        self.export_csv_BT.clicked.connect(lambda: self.export_csv())
        self.odt_CB.activated.connect(lambda: self.set_odt())
        self.close_BT.clicked.connect(quit_app)
        self.clearRIDs_BT.clicked.connect(lambda: self.clear_ids())
        self.kitsuURL.setText(config['kitsu']['server'])

        self.messages_TE.setReadOnly(True)

        sys.stdout = EmittingStream()
        sys.stdout.msg.connect(self.message)

        initial_message = ""
        initial_message += 'PROJECT PARAMETERS:\n'
        for k, v in config['project'].items():
            initial_message += "%s: %s\n" % (k, v)
        initial_message += '\nKITSU PARAMETERS:\n'
        for k, v in config['kitsu'].items():
            initial_message += "%s: %s\n" % (k, v)

        self.message(initial_message)
        self.message("Resolve is running!")

    def message(self, s):
        self.messages_TE.append(s)

    def name_shots(self):
        from resolve_tools.resolve_shots_ids import shots_ids
        self.messages_TE.clear()
        if self.process is None:
            dry = self.dryrun_CKB.isChecked()
            self.message("Creating Resolve VFX Shots IDs...")
            self.message("Dry run: " + str(dry))
            seq = self.seq_CB.currentText()
            clip_color = self.clipcolor_CB.currentText()
            flag_color = self.flag_CB.currentText()
            mode = self.createas_CB.currentText()
            shot_index_toggle = self.start_index_CKB.isChecked()
            shot_index = int(self.start_index_LE.text())
            if shot_index_toggle:
                shots_ids(mode, clip_color, flag_color, seq, shot_index, dry)
            else:
                shots_ids(mode, clip_color, flag_color, seq, 0, dry)

    def kitsu_create_shots(self):
        from kitsu_tools import kitsu_shots, kitsu_connect

        self.messages_TE.clear()
        if self.process is None:
            dry = self.dryrun_CKB.isChecked()
            self.message("Creating Kitsu shots entries...")
            self.message("Dry run: " + str(dry))
            proj = self.proj_TE.text()
            seq = self.seq_CB.currentText()
            clip_color = self.clipcolor_CB.currentText()
            config = self.config
            shot_index_toggle = self.start_index_CKB.isChecked()
            shot_index = int(self.start_index_LE.text())
            kitsu_url = self.kitsuURL.text()
            kitsu_connect.get_kitsu(kitsu_url)
            if shot_index_toggle:
                kitsu_shots.create_shot(config, proj, seq, clip_color, shot_index, dry)
            else:
                kitsu_shots.create_shot(config, proj, seq, clip_color, 0, dry)

    def clear_ids(self):
        from resolve_tools.resolve_shots_ids import clear_ids
        self.messages_TE.clear()
        if self.process is None:
            dry = self.dryrun_CKB.isChecked()
            self.message("Clearing Resolve VFS IDs...")
            self.message("Dry run: " + str(dry))
            clip_color = self.clipcolor_CB.currentText()
            flag_color = self.flag_CB.currentText()
            mode = self.createas_CB.currentText()
            seq = self.seq_CB.currentText()
            clear_ids(clip_color, flag_color, seq, mode, dry)

    def create_folders(self):
        self.messages_TE.clear()
        pass

    def render_jobs(self):
        from resolve_tools.resolve_deliver import vfx_plate_job
        self.messages_TE.clear()
        if self.process is None:
            self.message("Creating VFX Plates Jobs")
            dry = self.dryrun_CKB.isChecked()
            # proj = self.proj_TE.text()
            seq = self.seq_CB.currentText()
            # rnd = self.render_CKB.isChecked()
            clipcolor = self.clipcolor_CB.currentText()
            flagcolor = self.flag_CB.currentText()
            job_preset = self.job_presets_CB.currentText()
            config = self.config
            shot_index_toggle = self.start_index_CKB.isChecked()
            shot_index = int(self.start_index_LE.text())
            if shot_index_toggle:
                vfx_plate_job(config, clipcolor, flagcolor, seq, shot_index, job_preset, dry)
            else:
                vfx_plate_job(config, clipcolor, flagcolor, seq, 0, job_preset, dry)

    def print_preset(self):
        p = self.job_presets_CB.currentText()
        return p

    def process_finished(self):
        self.message("Process finished")
        self.process = None

    def set_odt(self):
        from resolve_tools.resolve_utils import render_odt
        self.messages_TE.clear()
        if self.process is None:
            dry = False
            self.message("Setting Resolve ODT to:")
            self.message("Dry run: " + str(dry))
            odt = self.odt_CB.currentText()
            self.message(odt)
            render_odt(odt)

    def export_csv(self):
        from resolve_tools.resolve_export_csv import export_csv
        self.messages_TE.clear()
        if self.process is None:
            dry = self.dryrun_CKB.isChecked()
            self.message("Exporting Shots CSV file to:")
            config = self.config
            self.message(config['kitsu']['config_folder'])
            self.message("Dry run: " + str(dry))
            seq = self.seq_CB.currentText()
            clip_color = self.clipcolor_CB.currentText()
            export_csv(seq, clip_color, dry)


class EmittingStream(QtCore.QObject):
    msg = QtCore.Signal(str)

    def write(self, text):
        self.msg.emit(str(text))

    def flush(self):
        pass


def run(project):
    app = QtWidgets.QApplication()

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(dark_palette)

    qt_app = PrjApp(project)
    qt_app.show()
    app.exec()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tools to helt with VFX shot work in Davinci Resolve')
    parser.add_argument('-p', '--project',
                        action="store",
                        dest="project",
                        help='VFX Project name')

    # parser.add_argument('-c', '--config',
    #                     action="store",
    #                     dest="config",
    #                     default='./example_project/config/config.yaml',
    #                     help='Image sequence or movie clip')
    #
    # parser.add_argument('-d', '--directory',
    #                     action="store",
    #                     dest="directory",
    #                     default='./example_project',
    #                     help='Image sequence or movie clip')
    #
    # parser.add_argument('-n', '--dry_run',
    #                     action="store_true",
    #                     dest="dry_run",
    #                     help='Print results but dont do anything')

    args = parser.parse_args()

    if args.project:
        project_name = args.project
        os.environ['RST_PROJ'] = project_name
        run(project_name)
        print("Project set")
    else:
        print("PROJ set to .example_project/\nPlease provide --project argument")
        sys.exit()
