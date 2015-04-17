from common import command
import os


def define(signature_builder):
        assert isinstance(signature_builder, command.SignatureBuilder)
        signature_builder\
            .title("Reboot")\
            .about("Reboot computer.")


def execute(context, args_map, log):
        assert isinstance(context, command.ExecutionContext)
        if 0 != os.system('shutdown /r /t 0 /f'):
            context.message("Reboot fails", "Something goes wrong reboot fails")
        else:
            context.message("Rebooting...", "Going to reboot computer, now")
