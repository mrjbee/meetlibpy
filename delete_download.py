from common import command
import os


def define(signature_builder):
    assert isinstance(signature_builder, command.SignatureBuilder)
    signature_builder\
        .title("Delete Download")\
        .about("Allow to delete downloaded file by specifying pattern which be a part of rm command. IMPORTANT! Its not allowed to include sign '//' and '..' as it might lead to unexpected behaviour ;)")\
        .args().text_arg(True, "pattern", "Rm like file pattern. IMPORTANT! Its not allowed to include sign '/' and '..' as it might lead to unexpected behaviour ;)")


def execute(context, args_map, log):
    assert isinstance(context, command.ExecutionContext)
    download_folder = "/opt/downloads"
    if "|" in args_map["pattern"]:
        context.message("Pattern error", "'&' cheating not allowed")
        return
    if "&" in args_map["pattern"]:
        context.message("Pattern error", "'&' cheating not allowed")
        return
    if ".." in args_map["pattern"]:
        context.message("Pattern error", "'..' is not allowed")
        return
    if "/" in args_map["pattern"]:
        context.message("Pattern error", "'/' is not allowed")
        return
    file_to_remove = download_folder+"/"+args_map["pattern"]
    if 0 != os.system("rm -rf "+file_to_remove):
        context.message("Fail to execute", "rm -rf "+file_to_remove)
    else:
        context.message("Executed", "rm -rf "+file_to_remove)

