# AlertFetcher
Simple script for fetching alert source events and non alerting events, then processing them into the `jsonl` data for use with Llama.

## Usage
### Environment
#### Python Packages
Install required packages with:

```pip install -r requirements.tx```

#### .env file
The script requires a file called `.env` with the following format:

```
ES_URL=<Elastic API URL>
API_KEY=<Elastic API Key>
```
#### config.json
`exclude`: Contains a list of json paths to remove from events before writing to the output.

### Running

To get alert source events and events which did not trigger an event 
during a time period (defaulting to the last 5 hours)
```
python3 AlertFetcher.py out=<output file> index=[alert index pattern] end=[ISO Timestamp] start=[ISO Timestamp]
```

`end` and `start` specify the timeperiod to search through for alerts/events 
(note that for alerts this searches the time alert was created not the source event).

`index` specifies a pattern for indices to search for alerts, by default it is `.internal.alerts-security.alerts-default-*`. 

`out` specifies a file to output the `jsonl` data to. **This is the only required argument.**

