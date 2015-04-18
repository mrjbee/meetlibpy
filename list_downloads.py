from common import command
import os


def define(signature_builder):
    assert isinstance(signature_builder, command.SignatureBuilder)
    signature_builder\
        .title("List Downloads")\
        .action("Show Download Content")\
        .about("Lists all files and folder inside download folder")


def execute(context, args_map, log):
    assert isinstance(context, command.ExecutionContext)
    download_folder = "/opt/downloads"
    files = os.listdir(download_folder)

    if len(files) == 0:
        context.message("No files in folder", download_folder)
        return

    context.message("Download folder", download_folder)
    result_list = context.message_list("Download folder content")
    for it_file in files:
        if os.path.isfile(os.path.join(download_folder, it_file)):
            size = os.path.getsize(os.path.join(download_folder, it_file))
            details_string = "Type: file Size: "+bytes2human(size)
        else:
            details_string = "Type: Folder"
        result_list.add(it_file, details_string)


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