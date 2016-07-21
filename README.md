# luigi-slack
Luigi tasks for Slack conversations ingestion, usfeul for NLP conversational training and design process

## What this does?
Do you want to generate real corpus to training chatterbots?  You need real conversations to feed your training.  Slack is a good platform, like many others, to emulate real conversations between experts and users simulating a "chatterbot user experience".
This first source code will help you to extract an entire conversation from a Slack Channel and dump it easily to a ```.tsv``` file.  The rest of the magic is yours.

## How to start

### Installation

```$ pip install luigi slackclient```

```$ luigid```

```$ open http://localhost:8082```

### Run Tasks

#### Setup config / help

```$ export PYTHONPATH=''```

```$ export SLACK_CLIENT_TOKEN="xoxp-1234567-12345678..............."``` (get your token from https://api.slack.com/web#authentication)

```$ luigi --module tasks  --help-all```

#### Extract Full Channel History in .tsv format

```$ luigi --module tasks  DownloadSlackChannelHistory --DownloadSlackChannelHistory-channel-name "general"```

![](https://github.com/gerardobort/luigi-slack/blob/master/doc/luigid-preview.png)
![](https://github.com/gerardobort/luigi-slack/blob/master/doc/luigid-preview2.png)

#### Generate Chatterbot corpus from a Slack Channel

@see Chatterbot project here: https://github.com/gunthercox/ChatterBot

```$ luigi --module tasks GenerateChatterbotCorpusFromSlackChannel --GenerateChatterbotCorpusFromSlackChannel-channel-name "general"```

