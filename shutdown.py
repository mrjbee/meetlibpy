from common import command
import os


def define(signature_builder):
    assert isinstance(signature_builder, command.SignatureBuilder)
    signature_builder \
        .title("Shutdown") \
        .about("This will shutdown your computer") \
        .args() \
        .text_arg(True, "TIME",
                  "TIME may have different formats, the most common is simply the word 'now'" +
                  " which will bring the system down immediately.  Other valid formats are +m," +
                  " where m is the number of minutes to wait until shutting down and hh:mm which" +
                  " specifies the time on the 24hr clock.")


def execute(context, args_map, log):
    assert isinstance(context, command.ExecutionContext)
    if 0 != os.system('shutdown '+args_map["TIME"]):
        context.message("Shutdown fails", "Something goes wrong reboot fails")
    else:
        context.message("Shutdown...", "Going to shutdown computer")
