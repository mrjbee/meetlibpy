import re
import shutil
from common import command
import os


def define(signature_builder):
    assert isinstance(signature_builder, command.SignatureBuilder)
    choice_builder = signature_builder\
        .title("Delete Downloaded File")\
        .about("Allow to delete downloaded file form existing list")\
        .args().arg_choices(True, "remove_file", "File to remove", "Please choose which file you are going to remove")

    assert isinstance(choice_builder, command.ChoiceArgumentDefinition)
    download_folder = "/opt/downloads"
    for it_file in os.listdir(download_folder):
        if os.path.isfile(os.path.join(download_folder, it_file)):
            size = os.path.getsize(os.path.join(download_folder, it_file))
            details_string = "Type: file Size: "+bytes2human(size)
        else:
            details_string = "Type: Folder"
        choice_builder.choice(it_file, details_string, it_file)

def execute(context, args_map, log):
    assert isinstance(context, command.ExecutionContext)
    download_folder = "/opt/downloads"
    purge(download_folder, args_map["remove_file"], context)


def purge(dir, file_name, context):
    assert isinstance(context, command.ExecutionContext)
    file_to_remove = os.path.join(dir, file_name)
    if not os.path.exists(file_to_remove):
        context.message("File not found", file_name)
        return

    if os.path.isfile(file_to_remove):
        os.remove(file_to_remove)
        context.message("File removed", file_name)
    else:
        shutil.rmtree(file_to_remove)
        context.message("Folder removed", file_name)


def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n