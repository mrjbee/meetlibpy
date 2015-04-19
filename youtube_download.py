# -*- coding: utf-8 -*-
from __future__ import division
import httplib, urllib, sys, os
from HTMLParser import HTMLParser
from time import sleep
from common import command

def define(signature_builder):
    assert isinstance(signature_builder, command.SignatureBuilder)
    signature_builder\
        .title("Youtube Download")\
        .action("Start download")\
        .about("Allows to download videos from youtube")\
        .args().arg_text(True, "url", "Youtube Link", "Link to youtube page with video")\
               .arg_choices(False, "quality", "Video Quality", "Quality of video to download. By default 'Medium Quality' is selected quality")\
                    .choice("High Quality", "720p or more but only if exists", "3")\
                    .choice("Medium Quality", "360p", "2")\
                    .choice("Low Quality", "", "1")



def execute(context, args_map, log):
    assert isinstance(context, command.CommandExecutionContext)
    requested_quality = int(args_map.get("quality", "2"))
    requested_type = None
    requested_url = args_map["url"]

    conn = httplib.HTTPSConnection("savedeo.com")
    conn.request("GET", "/download?url=" + requested_url)
    response = conn.getresponse()
    data = response.read()

    # HOTFIX (unicode issue): no idea why decode here help
    # data = data.decode('utf-8')
    parser = GetVideoParser()
    parser.feed(data)

    download_options = []

    for option in parser.optionList:
        if option.is_valid() and option.mp4_or_3gp() and option.quality() == requested_quality:
            download_options.append(option)

    if len(download_options) == 0:
        # Exit with showing options
        context.message("Download failed", "No video for requested quality")
        list_def = context.message_list("Available qualities")
        assert isinstance(list_def, command.MessageListResult)
        for option in parser.optionList:
            if option.is_valid() and option.mp4_or_3gp():
                list_def.add(option.quality_description(), option.quality_as_human())
        return

    download_options.sort(key=lambda option: option._quality_choice)
    download_option = download_options[0]
    context.message("Selected for download", download_option.quality_description()+" ("+download_option.quality_as_human()+")")
    # Actual downloading should start here
    context.sub_task(DownloadTask(download_option))
    return


class DownloadTask (command.Task):

    def __init__(self, option):
        super(DownloadTask, self).__init__()
        self._option = option

    def title(self):
        option = self._option
        assert isinstance(option, Option)
        return "Downloading ["+option._caption+" "+option.quality_description()+"]"

    def execute(self, context, log):
        self._context = context
        assert isinstance(context, command.TaskExecutionContext)
        option = self._option
        assert isinstance(option, Option)
        file_to_download = os.path.join(context.property("youtube_download"), option._caption+".part."+option._type).encode('utf-8')
        file_to_save = os.path.join(context.property("youtube_download"), option._caption+"."+option._type).encode('utf-8')
        urllib.urlretrieve(option._link, file_to_download, reporthook=self.dlProgress)
        os.rename(file_to_download, file_to_save)

    def dlProgress(self, count, blockSize, totalSize):
        context = self._context
        assert isinstance(context, command.TaskExecutionContext)
        percent = (count * blockSize)/totalSize
        if percent > 1:
            percent = 1
        context.progress(percent)


class Option:
    def __init__(self, caption, type_string, link, qualityString):

        if type_string.__contains__("mp4"):
            self._type = "mp4"
        elif type_string.__contains__("webm"):
            self._type = "webm"
        elif type_string.__contains__("3gp"):
            self._type = "3gp"
        elif type_string.__contains__("flv"):
            self._type = "flv"
        elif type_string.__contains__("m4a"):
            self._type = "m4a"
        else:
            self._type = None

        self._caption = caption
        if self._type:
            self._file_name = caption+"."+self._type
        self._link = link

        if qualityString.__contains__("1280x720"):
            self._quality_description = "1280x720"
            self._quality_choice = 1
            self._quality = 3
        elif qualityString.__contains__("640x360"):
            self._quality_description = "640x360"
            self._quality_choice = 1
            self._quality = 2
        elif qualityString.__contains__("320x240"):
            self._quality_description = "320x240"
            self._quality_choice = 2
            self._quality = 1
        elif qualityString.__contains__("176x144"):
            self._quality_description = "176x144"
            self._quality_choice = 1
            self._quality = 1
        else:
            self._quality_choice = None
            self._quality = None

    def is_valid(self):
        return self._link and self._type is not None and self._quality is not None

    def mp4_or_3gp(self):
        return self._type is "3gp" or self._type is "mp4"

    def quality(self):
        return self._quality

    def quality_as_human(self):
        if self._quality is 3:
            return "High Quality"
        elif self._quality is 2:
            return "Medium Quality"
        elif self._quality is 1:
            return "Low Quality"
        return "Unknown Quality"

    def quality_description(self):
        return self._quality_description

    def choice(self):
        return self._quality_choice


class GetVideoParser(HTMLParser):
    def __init__(self):
        self.optionList = []
        self._caption = None
        self._isCaptionTag = False
        self._isCaptionData = False
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and len(attrs) == 1:
            if attrs[0][1] == 'main':
                self._isCaptionTag = True
                return

        if self._isCaptionTag and tag == 'h1':
            self._isCaptionData = True

        if tag == 'a' and len(attrs) > 1 and attrs[0][0] == 'data-event' and not attrs[0][1].__contains__("DASH Video"):
            option = Option(self._caption, attrs[0][1], attrs[1][1], attrs[0][1])
            self.optionList.append(option)

    def handle_data(self, data):
        if self._isCaptionData:
            # HOTFIX (unicode issue): no idea why encode here help
            self._caption = data.strip().decode('utf-8')
            self._isCaptionTag = False
            self._isCaptionData = False
