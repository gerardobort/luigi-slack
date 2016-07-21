from __future__ import print_function
import json
import requests
import luigi
import datetime
import re
from slack import *

## WIP - conversations have to be sampled by date, topic or something else
class GenerateChatterbotCorpusFromSlackChannel(luigi.Task):

    channel_name = luigi.Parameter()
    date = luigi.DateParameter(default=datetime.date.today())

    def requires(self):
        return DownloadSlackChannelHistory(date=self.date, channel_name=self.channel_name)

    def run(self):

        corpus = { "conversations": [] }
        with self.input().open('r') as infile:
            messages = [line.strip().split('\t')[-1:][0] for line in infile]
            messages.reverse()
            corpus["conversations"] = [messages]

        with self.output().open('w') as outfile:
            json.dump(corpus, outfile, sort_keys=True, indent=4, separators=(',', ': '))

    def output(self):
        return luigi.LocalTarget(self.date.strftime('data/Chatterbot/Corpus/' + self.channel_name + '_%Y-%m-%d.json'))
