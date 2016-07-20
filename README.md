# luigi-slack
Luigi tasks for Slack conversations ingestion, usfeul for NLP conversational training and design process

## How to start

### Installation

```$ pip install luigi```

```$ luigid```

```$ open http://localhost:8082```

### Run Tasks

```$ export PYTHONPATH=''```

```$ luigi --module tasks  --help-all```

```$ luigi --module tasks  DownloadSlackChannelHistory --DownloadSlackChannelHistory-channel-name "general"```

