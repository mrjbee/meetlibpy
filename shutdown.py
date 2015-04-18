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
    time_arg = args_map["TIME"]
    if time_arg == "now":
        do_shutdown(time_arg, context)
    else:
        task = ShutdownTask(time_arg)
        context.message("Shutdown scheduled", "Shutdown going to be executed later as accordingly to time argument ("+time_arg+")")
        context.sub_task(task)


def do_shutdown(time, context):
    if 0 != os.system('shutdown -h '+time):
        context.stop("Something goes wrong shutdown fails")
        return False
    else:
        context.message("Shutdown...", "Going to shutdown computer")
        return True


class ShutdownTask (command.Task):

    def __init__(self, time):
        super(ShutdownTask, self).__init__()
        self._time = time

    def title(self):
        return "Shutdown with "+self._time

    def execute(self, context, log):
        assert isinstance(context, command.TaskExecutionContext)
        context.progress(0.2)
        do_shutdown(self._time, context)
        context.progress(1)
