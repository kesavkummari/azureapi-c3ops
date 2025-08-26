import logging
import azure.functions as func

from azure.identity import ManagedIdentityCredential
from azure.mgmt.compute import ComputeManagementClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure Function - List VMs started')

    try:
        # Get subscription ID (set in Function App config)
        subscription_id = "<YOUR_SUBSCRIPTION_ID>"  

        # Authenticate using Managed Identity
        credential = ManagedIdentityCredential()
        compute_client = ComputeManagementClient(credential, subscription_id)

        # List all VMs
        vm_list = []
        for vm in compute_client.virtual_machines.list_all():
            vm_info = {
                "name": vm.name,
                "location": vm.location,
                "os_type": vm.storage_profile.os_disk.os_type.value
            }
            vm_list.append(vm_info)

        return func.HttpResponse(str(vm_list), status_code=200)

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse("Error listing VMs: " + str(e), status_code=500)
