import re
import shutil
from common import command
import os


def define(signature_builder):
    assert isinstance(signature_builder, command.SignatureBuilder)
    signature_builder\
        .title("Sort Youtube")\
        .about("Allow to move downloaded file to subfolders which allows to categorize downloads")\
        .args()\
            .arg_text(False, "new_folder", "New folder", "Allows to create new folder if set", "Health")
    download_folder = signature_builder.property("youtube_download")

    folder_chooser = signature_builder.args().arg_choices(True, "folder", "Folder to move", "Please choose in which folder file would be moved. Select new folder in case you want to create new")
    assert isinstance(folder_chooser, command.ChoiceArgumentDefinition)
    file_chooser = signature_builder.args().arg_choices(True, "file", "File to move", "Please select file to move")
    assert isinstance(file_chooser, command.ChoiceArgumentDefinition)

    if download_folder is None:
        folder_chooser.choice("Un supported", "Server doesn`t support youtube downloads", "no_support")
        file_chooser.choice("Un supported", "Server doesn`t support youtube downloads", "no_support")
        return

    folder_chooser.choice("New folder", "Create new and move there",  "new_folder")

    for it_file in os.listdir(download_folder):
        if os.path.isfile(os.path.join(download_folder, it_file)):
            if ".part." not in it_file:
                file_chooser.choice(it_file, "", it_file)
        else:
            folder_chooser.choice(it_file, "", it_file)


def execute(context, args_map, log):
    pass