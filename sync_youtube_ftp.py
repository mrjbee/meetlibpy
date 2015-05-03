# -*- coding: utf-8 -*-

import http.client, urllib.request, urllib.parse, urllib.error, sys, os, ftplib
from html.parser import HTMLParser
from time import sleep
from common import command

def define(signature_builder):
    assert isinstance(signature_builder, command.SignatureBuilder)
    signature_builder\
        .title("Synchronize Youtube")\
        .action("Start Synchronization")\
        .about("Allows synchronize downloaded video to ftp folder")


def execute(context, args_map, log):
    assert isinstance(context, command.CommandExecutionContext)
    download_folder = context.property("youtube_download")
    result_file_list = context.message_list("Files to synchronize")
    assert isinstance(result_file_list, command.MessageListResult)
    files_to_sync = []
    for file in os.listdir(download_folder):
        if (".part." not in file) and (file.endswith(".mp4") or file.endswith(".3gp")):
            result_file_list.add(file)
            files_to_sync.append(file)

    for sync_file in files_to_sync:
        context.sub_task(SynchronizationTask(sync_file,os.path.join(download_folder,sync_file)))


class SynchronizationTask (command.Task):

    def __init__(self, file_name, file_path):
        super(SynchronizationTask, self).__init__()
        self._file_name = file_name.encode("utf-8")
        self._file_path = file_path.encode("utf-8")

    def title(self):
        return "Synchronizing ["+self._file_name+"]"

    def execute(self, context, log):
        self._context = context
        assert isinstance(context, command.TaskExecutionContext)
        ftp_details = context.property("youtube.sync.ftp")
        ftp = ftplib.FTP(ftp_details["address"])
        try:
            ftp.login(ftp_details["user"], ftp_details["password"])
            ftp.cwd(ftp_details["folder"])
            data = []
            ftp.dir(data.append)
            for remote_file_details in data:
                if self._file_name in remote_file_details:
                    os.remove(self._file_path)
                    return
            ftp.storbinary("STOR " + self._file_name+".ftp", open(self._file_path, "rb"), 1024)
            ftp.rename(self._file_name+".ftp", self._file_name)
            ftp.quit()
            ftp = None
            os.remove(self._file_path)
        finally:
            if ftp:
                ftp.quit()
        # urllib.urlretrieve(option._link, file_to_download, reporthook=self.dlProgress)
        # os.rename(file_to_download, file_to_save)

    def dlProgress(self, count, blockSize, totalSize):
        context = self._context
        assert isinstance(context, command.TaskExecutionContext)
        percent = (count * blockSize)/totalSize
        if percent > 1:
            percent = 1
        context.progress(percent)
