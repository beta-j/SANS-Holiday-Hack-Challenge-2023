# OBJECTIVE 5 - Azure 101 #

## OBJECTIVE : ##
>Help Sparkle Redberry with some Azure command line skills.  Find the elf and the terminal on Christmas Island.
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 5</summary>
  
>-	The Azure CLI tools come with a builtin help system, but Microsoft also provides this [handy cheatsheet](https://learn.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest).
</details>

#  

## PROCEDURE : ##

>You may not know this but the Azure cli help messages are very easy to access.  First, try typing: $ az help | less

`~$ az help | less`

>Next, you've already been configured with credentials. Use 'az' and your 'account' to 'show' your current details and make sure to pipe to less ( | less ) 

`~$ az account show | less`
```
{
  "environmentName": "AzureCloud",
  "id": "2b0942f3-9bca-484b-a508-abdae2db5e64",
  "isDefault": true,
  "name": "northpole-sub",
  "state": "Enabled",
  "tenantId": "90a38eda-4006-4dd5-924c-6ca55cacc14d",
  "user": {
    "name": "northpole@northpole.invalid",
    "type": "user"
  }
}
```

>Excellent! Now get a list of resources in Azure.  For more information: [https://learn.microsoft.com/en-us/cli/azure/group?view=azure-cli-latest](https://learn.microsoft.com/en-us/cli/azure/group?view=azure-cli-latest)

`~$ az group list`

```
  {
    "id": "/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64/resourceGroups/northpole-rg1",
    "location": "eastus",
    "managedBy": null,
    "name": "northpole-rg1",
    "properties": {
      "provisioningState": "Succeeded"
    },
    "tags": {}
  },
  {
    "id": "/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64/resourceGroups/northpole-rg2",
    "location": "westus",
    "managedBy": null,
    "name": "northpole-rg2",
    "properties": {
      "provisioningState": "Succeeded"
    },
    "tags": {}
  }
```

> Ok, now use one of the resource groups to get a list of function apps. For more information:
[https://learn.microsoft.com/en-us/cli/azure/functionapp?view=azure-cli-latest](https://learn.microsoft.com/en-us/cli/azure/functionapp?view=azure-cli-latest)
Note: Some of the information returned from this command relates to other cloud assets used by Santa and his elves.

`~$ az functionapp list –-resource-group northpole-rg1`

>Find a way to list the only VM in one of the resource groups you have access to.
>For more information: [https://learn.microsoft.com/en-us/cli/azure/vm?view=azure-cli-latest](https://learn.microsoft.com/en-us/cli/azure/vm?view=azure-cli-latest)

`~$ az vm list –g northpole-rg2`

>Find a way to invoke a run-command against the only Virtual Machine (VM) so you can RunShellScript and get a directory listing to reveal a file on the Azure VM.
>For more information: [https://learn.microsoft.com/en-us/cli/azure/vm/run-command?view=azure-cli-latest#az-vm-run-command-invoke](https://learn.microsoft.com/en-us/cli/azure/vm/run-command?view=azure-cli-latest#az-vm-run-command-invoke)

`~$ az vm run-command invoke -g northpole-rg2 -n NP-VM1 –comand-id RunShellScript –scripts ‘ls’`

>Great, you did it all!

