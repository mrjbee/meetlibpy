import re
import shutil
from common import command
import os


def define(signature_builder):
    assert isinstance(signature_builder, command.SignatureBuilder)
    signature_builder\
        .title("Delete Download")\
        .about("Allow to delete downloaded file by specifying pattern.")\
        .args().text_arg(True, "pattern", "Specify pattern for matching file")


def execute(context, args_map, log):
    assert isinstance(context, command.ExecutionContext)
    download_folder = "/opt/downloads"
    purge(download_folder, args_map["pattern"], context)


def purge(dir, pattern, context):
    assert isinstance(context, command.ExecutionContext)
    for f in os.listdir(dir):
        if re.search(pattern, f):
            file_to_remove = os.path.join(dir, f)
            if os.path.isfile(file_to_remove):
                os.remove(file_to_remove)
                context.message("File removed", file_to_remove)
            else:
                shutil.rmtree(file_to_remove)
                context.message("Folder removed", file_to_remove)