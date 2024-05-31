#!/usr/bin/env python

import os
import sys
import argparse

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

from ui import rst_ui as window
from proj_tools.proj_data import Config
from resolve_tools.resolve_utils import ResolveUtils
from resolve_tools.resolve_shots_ids import ShotIdentifier
from resolve_tools.resolve_deliver import vfx_plate_job
from resolve_tools.resolve_export_csv import export_csv
from kitsu_tools import kitsu_shots, kitsu_connect


class RST_App(window.Ui_main_window, QtWidgets.QMainWindow):
    def __init__(self, project):
        super(RST_App, self).__init__()
        self.config = Config().get_config()
        self.resolve_utils = ResolveUtils()
        self.shot_identifier = ShotIdentifier()
        config = self.config
        self.render_presets = self.dr_render_presets()
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

        resolve_version = self.resolve_utils.get_resolve_version()
        self.message(f"Resolve is connected.\n{resolve_version}\n")

        initial_message = self.get_initial_message(config)
        self.message(initial_message)

    def get_initial_message(self, config):
        initial_message = "PROJECT PARAMETERS:\n"
        for k, v in config['project'].items():
            initial_message += f"{k}: {v}\n"

        # initial_message += "\nRESOLVE PARAMETERS:\n"
        # for k, v in config['resolve'].items():
        #     initial_message += f"{k}: {v}\n"

        initial_message += "\nKITSU PARAMETERS:\n"
        for k, v in config['kitsu'].items():
            initial_message += f"{k}: {v}\n"
        return initial_message

    def dr_render_presets(self):
        render_presets = self.resolve_utils.render_presets()
        presets = [v for k, v in sorted(render_presets.items())]
        return presets

    def message(self, s):
        self.messages_TE.append(s)

    def name_shots(self):
        self.messages_TE.clear()
        if self.process is None:
            dry = self.dryrun_CKB.isChecked()
            self.message("Creating Resolve VFX Shots IDs...")
            self.message(f"Dry run: {dry}")
            seq = self.seq_CB.currentText()
            clip_color = self.clipcolor_CB.currentText()
            flag_color = self.flag_CB.currentText()
            mode = self.createas_CB.currentText()
            shot_index_toggle = self.start_index_CKB.isChecked()
            shot_index = int(self.start_index_LE.text())
            index_offset = shot_index if shot_index_toggle else 0
            self.shot_identifier.shots_ids(mode, clip_color, flag_color, seq, index_offset, dry)

    def kitsu_create_shots(self):
        self.messages_TE.clear()
        if self.process is None:
            dry = self.dryrun_CKB.isChecked()
            self.message("Creating Kitsu shots entries...")
            self.message(f"Dry run: {dry}")
            proj = self.proj_TE.text()
            seq = self.seq_CB.currentText()
            clip_color = self.clipcolor_CB.currentText()
            config = self.config
            shot_index_toggle = self.start_index_CKB.isChecked()
            shot_index = int(self.start_index_LE.text())
            kitsu_url = self.kitsuURL.text()
            kitsu_connect.get_kitsu(kitsu_url)
            index_offset = shot_index if shot_index_toggle else 0
            kitsu_shots.create_shot(config, proj, seq, clip_color, index_offset, dry)

    def clear_ids(self):
        self.messages_TE.clear()
        if self.process is None:
            dry = self.dryrun_CKB.isChecked()
            self.message("Clearing Resolve VFS IDs...")
            self.message(f"Dry run: {dry}")
            clip_color = self.clipcolor_CB.currentText()
            flag_color = self.flag_CB.currentText()
            mode = self.createas_CB.currentText()
            seq = self.seq_CB.currentText()
            self.shot_identifier.clear_ids(clip_color, flag_color, seq, mode, dry)

    def render_jobs(self):
        self.messages_TE.clear()
        if self.process is None:
            self.message("Creating VFX Plates Jobs")
            dry = self.dryrun_CKB.isChecked()
            seq = self.seq_CB.currentText()
            clipcolor = self.clipcolor_CB.currentText()
            flagcolor = self.flag_CB.currentText()
            job_preset = self.job_presets_CB.currentText()
            config = self.config
            shot_index_toggle = self.start_index_CKB.isChecked()
            shot_index = int(self.start_index_LE.text())
            index_offset = shot_index if shot_index_toggle else 0
            vfx_plate_job(config, clipcolor, flagcolor, seq, index_offset, job_preset, dry)

    def set_odt(self):
        self.messages_TE.clear()
        if self.process is None:
            odt = self.odt_CB.currentText()
            self.resolve_utils.render_odt(odt)

    def export_csv(self):
        self.messages_TE.clear()
        if self.process is None:
            dry = self.dryrun_CKB.isChecked()
            self.message("Exporting Shots CSV file to:")
            config = self.config
            self.message(config['kitsu']['config_folder'])
            self.message(f"Dry run: {dry}")
            seq = self.seq_CB.currentText()
            clip_color = self.clipcolor_CB.currentText()
            shot_index_toggle = self.start_index_CKB.isChecked()
            shot_index = int(self.start_index_LE.text())
            index_offset = shot_index if shot_index_toggle else 0
            export_csv(seq, clip_color, index_offset, dry)


class EmittingStream(QtCore.QObject):
    msg = QtCore.Signal(str)

    def write(self, text):
        self.msg.emit(str(text))

    def flush(self):
        pass


def quit_app():
    print('CLEAN EXIT')
    QtWidgets.QApplication.quit()


def run(project):
    app = QtWidgets.QApplication(sys.argv)

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

    qt_app = RST_App(project)
    qt_app.show()
    app.exec()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tools to help with VFX shot work in DaVinci Resolve')
    parser.add_argument('-p', '--project', action="store", dest="project", help='VFX Project name')

    args = parser.parse_args()

    if args.project:
        project_name = args.project
        os.environ['RST_PROJ'] = project_name
        run(project_name)
        print("Project set")
    else:
        print("PROJ set to .example_project/\nPlease provide --project argument")
        sys.exit()
