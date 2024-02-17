# azure-key-vault-alert
[pip package](https://pypi.org/project/ops-py-azure-key-vault-alert)

---

## Description
Generates a **Key Vault Secret** status report using 
[ops-py-azure-key-vault-report](https://pypi.org/project/ops-py-azure-key-vault-report)
for one more **Key Vaults**.

Each report is posted continuously to **Slack** using
[ops-py-message-handler](https://pypi.org/project/ops-py-message-handler/)

When done, an optional final notify is sent to **Slack** using an additional webhook.

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

`--teams_output`  
If this argument is provided, a MS Teams json object of the report will be generated and used as the payload.

`--report_if_no_html`  
Will post the facts (summary report) to MS Teams even though no records in the html report   

`--title`  
The title of the message posted in Slack or MS Teams (Default: Azure Key Vault report)   

`--record_types`  
List of record types to check for. E.g. certificate secret  
Valid types are: certificate secret key (Default is all: certificate secret key)  

`--slack_max_chars`  
The max characters the report can have due to the Slack Workflow message limits (Default: 13081)   

`--teams_max_chars`  
The max characters the report can have due to the MS Teams payload size limits (Default: 22854)  

`--stdout_only`  
Only print report to stdout. No post to messagehandler (Slack or MS Teams")  


---

### Example on how to use this package in a GitHub Action Workflow:
**NOTE:** Use the predefined shared [azure-key-vault-alert](..%2F..%2F..%2Fdocs%2Fworkflows%2Fazure-key-vault-alert.md) workflow instead.

**Bash script**  
Create shell script which then is called by the pipeline, e.g. `key_vault_alert.sh` with the following content:
```
#!/bin/bash

BASEDIR=$(dirname "$0")

# To ensure that we are in the same directory as where this script is located
cd $BASEDIR

# Create a new empty Python virtual environment
python3 -m venv .venv

# Activate the newly created Python virtual environment
source .venv/bin/activate

# Only install the python packages specified in the requirements.txt files
pip install -r requirements.txt

# Executes ops-py-azure-key-vault-alert. Arguments are passed from this bash script to the python script
python3 -m azure_key_vault_alert.azure_key_vault_alert "$@"
```
Make sure to make the script executable before checking it in: `chmod +x key_vault_alert.sh`

**PIP requirements.txt file**  
Make sure to generate a `requirements.txt` file and check in:
```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip ops-py-azure-key-vault-alert
pip list --format=freeze > requirements.txt
git add requirements.txt 
```
More info about [Python virtual environment](https://github.com/equinor/ops-py/tree/main/tools)


**Pipeline steps**

- **Login to Azure CLI**  
  Make sure this step is done before calling the `azure-key-vault-alert`. Also make sure the client id has the privileges to list the desired Key Vault Secrets.  
  Example code of this step:
  ```
  - name: "Azure login"
    uses: azure/login@v1
    with:
      client-id: ${{ env.SERVICE_PRINCIPAL_CLIENT_ID }}
      subscription-id: ${{ env.SUBSCRIPTION_ID }}
      tenant-id: ${{ env.TENANT_ID }}
      enable-AzPSSession: true
  ```

- Execute the `key_vault_alert.sh` script:
  ```
  - name: Key Vault Secrets report to Slack
    run: ./key_vault_alert.sh -v kv-dev kv-qa
  ```
  Specify the list of desired key vault names after the `-v` argument. The key vault names must be separated by space.
