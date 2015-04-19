from common import command
import os


def define(signature_builder):
        assert isinstance(signature_builder, command.SignatureBuilder)
        signature_builder\
            .title("Boot In Windows")\
            .action("To Windows")\
            .about("Reboot computer your computer to a Windows OS")


def execute(context, args_map, log):
        assert isinstance(context, command.ExecutionContext)
        if 0 != os.system('grub-reboot 4'):
            context.message("Updating grub fails", "Could`t set grub option to 4")
            return
        else:
            context.message("Grub updated", "Grub updated to boot in option 4")

        if 0 != os.system('reboot now'):
            context.message("Reboot fails", "Something goes wrong reboot fails")
        else:
            context.message("Rebooting...", "Going to reboot computer, now")
