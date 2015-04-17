from common import command
import os


def define(signature_builder):
    assert isinstance(signature_builder, command.SignatureBuilder)
    signature_builder\
        .title("List Downloads")\
        .about("Lists all files and folder inside download folder")


def execute(context, args_map, log):
    assert isinstance(context, command.ExecutionContext)
    download_folder = "/opt/downloads"
    files = os.listdir(download_folder)
    if len(files) == 0:
        context.message("No files in folder", download_folder)
        return
    for file in files:
        context.message("Found", file)