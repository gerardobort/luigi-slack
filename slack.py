from __future__ import print_function
import json
import requests
import luigi
import datetime
import re
import os
from slackclient import SlackClient


class DownloadSlackChannelHistoryChunk(luigi.Task):

    channel_name = luigi.Parameter("")
    last_message_id = luigi.Parameter("")
    date = luigi.DateParameter(default=datetime.date.today())

    def run(self):
        # create one at https://api.slack.com/web#authentication, and set the environment variable
        sc = SlackClient(os.environ["SLACK_CLIENT_TOKEN"])
        channel_id = 0

        # Get Channel Information
        for channel in sc.api_call("channels.list")["channels"]:
            if (channel["name"] == self.channel_name):
                channel_id = channel["id"]

        # Get Channel History
        if (self.last_message_id):
            channel_history_chunk = sc.api_call("channels.history", channel=channel_id, count=1000, latest=self.last_message_id)
        else:
            channel_history_chunk = sc.api_call("channels.history", channel=channel_id, count=1000)
        
        if (not channel_history_chunk["ok"]):
            raise Exception('Channel not found, or permissions error', 'channel_name=' + self.channel_name)

        channel_history_chunk_last_message = channel_history_chunk["messages"]
        outputdata = channel_history_chunk
        with self.output().open('w') as outfile:
            json.dump(outputdata, outfile, sort_keys=True, indent=4, separators=(',', ': '))

    def output(self):
        return luigi.LocalTarget(self.date.strftime('data/Slack/ChannelHistory/' + self.channel_name + '/Chunk_' + str(self.last_message_id) + '_%Y-%m-%d.json'))


class DownloadSlackChannelHistory(luigi.Task):

    channel_name = luigi.Parameter()
    date = luigi.DateParameter(default=datetime.date.today())

    def run(self):
        # create one at https://api.slack.com/web#authentication, and set the environment variable
        sc = SlackClient(os.environ["SLACK_CLIENT_TOKEN"])
        channel_id = 0

        # Get Channel Information
        for channel in sc.api_call("channels.list")["channels"]:
            if (channel["name"] == self.channel_name):
                channel_id = channel["id"]

        if (0 == channel_id):
            raise Exception('Unable to find such channel by name', 'channel_name=' + self.channel_name)

        messages = []

        # Get the first chunk
        last_message_id = 0
        taskOutput = yield DownloadSlackChannelHistoryChunk(channel_name=self.channel_name)
        with taskOutput.open('r') as infile:
            last_chunk = json.load(infile)
            last_message_id = last_chunk["messages"][0]["ts"] # TODO check 4 failures
            messages += last_chunk["messages"]

        # Get more chunks
        while (last_chunk["has_more"]):
            taskOutput = yield DownloadSlackChannelHistoryChunk(channel_name=self.channel_name, last_message_id=last_message_id)
            with taskOutput.open('r') as infile:
                last_chunk = json.load(infile)
                last_message_id = last_chunk["messages"][0]["ts"] # TODO check 4 failures
                messages += last_chunk["messages"]

        messages.reverse()
        with self.output().open('w') as outfile:
            info = (
                "type",
                "ts",
                "user",
                "is_starred",
                "text",
            )
            print(*info, file=outfile, sep='\t')
            for message in messages:
                info = (
                    message["type"],
                    message["ts"],
                    message.get("user"),
                    message.get("is_starred"),
                    message.get("text").encode('ascii', 'ignore').replace("\n", "\\n").replace("\t", "\\t"),
                )
                print(*info, file=outfile, sep='\t')


    def output(self):
        return luigi.LocalTarget(self.date.strftime('data/Slack/ChannelHistory/' + self.channel_name + '_%Y-%m-%d.tsv'))
