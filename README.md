# AlertFetcher
Simple UI for fetching events from an Elastic SIEM and summarizing them using AI.

Originally forked from: https://github.com/IPG5/AlertFetch

## Usage
### Environment
Install required packages with:

```pip install -r requirements.txt```

### Config
#### config.json
`exclude`: dict where the keys are names of lists of fields for use in the `Field Exclusion` pane of the ui

`context_fields`: dict where the keys are names of lists of fields used in the `Context Fields` section of the `Grouping` Pane

`prompts`: list of prompts for use with AI in the `AI Summarizer` pane

#### apis.json
Dict of the form:
```json
{
  "<API_NAME>": {
    "key": "<API KEY>",
    "uri": "<API ENDPOINT>"
  }
}
```
This defines the apis that can be used in the API dropdown.

#### openai.json
Dict containing the details for the OpenAI API the AI summarizer will use.
```json
{
  "api_key": "<API KEY>",
  "base_url": "<API ENDPOINT>"
}
```
*note the base_url should probably end with `/v1`*

### Running

Launch the ui with: ```python ./AF_UI.py```