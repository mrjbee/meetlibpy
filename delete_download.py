import re
import shutil
from common import command
import os


def define(signature_builder):
    assert isinstance(signature_builder, command.SignatureBuilder)
    signature_builder\
        .title("Delete Download")\
        .about("Allow to delete downloaded file by specifying pattern.")\
        .args().arg_text(True, "pattern", "File mask", "Specify pattern for matching file", ".*.txt")\
        .arg_flag("dry_run", "'Dry Run' mode activated",
                  "'Dry Run' mode designed for pattern test. "
                  "In this mode you will affect no files "
                  "but will get clear understanding on what going to be deleted", True)



def execute(context, args_map, log):
    assert isinstance(context, command.ExecutionContext)
    download_folder = "/opt/downloads"
    if args_map["dry_run"]:
        context.message("'Dry Run' mode", "Activated")
    purge(download_folder, args_map["pattern"], args_map["dry_run"], context)


def purge(dir, pattern, do_dry, context):
    assert isinstance(context, command.ExecutionContext)
    for f in os.listdir(dir):
        if re.search(pattern, f):
            file_to_remove = os.path.join(dir, f)
            if os.path.isfile(file_to_remove):
                if not do_dry:
                    os.remove(file_to_remove)
                context.message("File removed", file_to_remove)
            else:
                if not do_dry:
                    shutil.rmtree(file_to_remove)
                context.message("Folder removed", file_to_remove)