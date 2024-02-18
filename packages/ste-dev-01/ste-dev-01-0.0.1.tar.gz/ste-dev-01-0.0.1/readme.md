# azure-key-vault-alert
[pip package](https://pypi.org/project/ops-py-azure-key-vault-alert)

---

## Description
Generates a **Key Vault Secret** status report and summary using 
[ops-py-azure-key-vault-report](https://github.com/equinor/ops-py-azure-key-vault-report)
for one more **Key Vaults**.

The summary and report may be posted to a Slack webhook (Slack App or Slack Webflow) or to MS Teams webhook.
When posting to MS Teams, a payload containing a html table will be used.

For Slack the message will be formatted as plaintext in standard Markdown format

If nothing to report, e.g. none of the records meets the criteria for reporting, only the summary will be posted.

Also, when done, an optional final notify may be posted to **Slack** using an additional webhook.

The post requests are handled by [ops-py-message-handler](https://github.com/equinor/ops-py-message-handler)

**Slack**  
If the url of the webhook contains `slack.com` the report will be posted to **Slack**.
- **Slack App**   
  If the webhook contains `slack.com/services` a payload for a Slack App will be generated in the following format:   
    ```
    *{title}*\n```{report}```
    ```
- **Slack Workflow**   
  If the webhook contains `slack.com`, but not the `slack.com/services` part, a payload for a Slack Webflow will
  be generated. The Workflow will have to be set to accept a `Title` variable and a `Text` variable.

**MS Teams**
- If the url of the webhook **does not** contain `slack.com` a payload for MS Teams will be generated. The payload will
also contain a html table of the report (if any). If nothing to report, only a summary will be posted as `facts`. 


## Installation
`pip install ops-py-azure-key-vault-alert`

---

## Usage
Export the **WEBHOOK_REPORT** Environment Variables:
  - `WEBHOOK_REPORT`  
    Each report is posted to the value of this webhook. E.g.:  
    `export WEBHOOK_REPORT="https://hooks.slack.com/workflows/T02XYZ..."`


  - `WEBHOOK_NOTIFY`  
    When all the reports have been posted, an additional POST is performed to the value of this webhook. E.g.:  
    `export WEBHOOK_NOTIFY="https://hooks.slack.com/workflows/T02ZYX..."`


Provide the list of key vaults to generate reports for after the `-v` / `--vaults`'  
command line argument (space separated) when **executing the code**. E.g.:   
`python3 azure_key_vault_alert -v kv-prod kv-dev kv-qa`

**Other valid arguments:**   
`--expire_threshold`     
If this argument is provided and followed by a int value (int),
the record will only be reported if days to the record's Expiration Date is below the threshold.

`--include_no_expiration`   
If this argument is provided, the report will also include the records which has no Expiration Date set.

`--include_all`  
If this argument is provided, the report will include all the records (verbose).

`--report_if_no_html`  
Will post the facts (summary report) to MS Teams even though no records in the html report   

`--title`  
The title of the message posted in Slack or MS Teams (Default: Azure Key Vault report)   

`--record_types`  
List of record types to check for. E.g. certificate secret  
Valid types are: certificate secret key (Default is all: certificate secret key)  

`--teams_max_chars`  
The max characters the report can have due to the MS Teams payload size limits (Default: 22854)  

`--stdout_only`  
Only print report to stdout. No post to messagehandler (Slack or MS Teams")  
