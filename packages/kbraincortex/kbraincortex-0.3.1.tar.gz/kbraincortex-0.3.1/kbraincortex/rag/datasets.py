import logging
from kbraincortex.azure.cosmos import query_cosmos_db
from kbraincortex.microsoft.graph import list_site_contents, on_behalf_of
from kbrainsdk.ingest import Ingest

def security_check_azure(dataset, token, email, client_id, oauth_secret, tenant_id):
    id = dataset["id"]
    logging.info(f"Validating access to Azure Storage Container {id}...")
    #client_id = os.getenv("CLIENT_ID")
    #client_secret = os.getenv("OAUTH_CLIENT_SECRET") 
    #scope = "https://storage.azure.com/user_impersonation"
    #access_token, _ = on_behalf_of(client_id, client_secret, token, scope)
    #validate_blob_access(access_token, site)
    whitelist = [
        "cliff.gornto@us.kbr.com",
        "richard.schindel@us.kbr.com",
        "byron.bright@us.kbr.com",
        "patrice.porter@us.kbr.com",
        "toni.shepard@kbr.com",
        "ruzanna.makaryan@us.kbr.com",
        "john.thomson@kbr.com",
        "callie.sepolio@kbr.com",
        "jeffrey.lehnertz@us.kbr.com",
        "jeff.hawks@us.kbr.com",
        "chris.bergey@us.kbr.com",
        "dustin.kanady@us.kbr.com",
        "richard.schwenk@us.kbr.com",
        "jason.gray@us.kbr.com",
        "dan.dawson@us.kbr.com",
        "reginald.hamilton@us.kbr.com",
        "megan.wagner@us.kbr.com",
        "todd.may@us.kbr.com",
        "marty.exline@us.kbr.com",
        "scot.butkis@us.kbr.com",
        "cheryl.quail@us.kbr.com",
        "michelle.cooper@us.kbr.com",
        "micah.webb@us.kbr.com",
        "douglas.hayes@us.kbr.com",
        "james.foulks@us.kbr.com",
        "jacob.gonzalez@us.kbr.com",
        "felicia.jones@us.kbr.com",
        "joseph.kennedy@us.kbr.com",
        "jay.lennon@us.kbr.com",
        "gregory.mecca@us.kbr.com",
        "geoffrey.pierce@us.kbr.com",
        "mattias.turner@us.kbr.com",
        "ben.ochoa@us.kbr.com",
        "patricia.nunn@us.kbr.com",
        "justin.mclellan@us.kbr.com",
        "shawn.schumacher@us.kbr.com",
        "michael.dawson@us.kbr.com",
        "daniel.lafevor@us.kbr.com",
        "julie.thomas@us.kbr.com",
        "ryan.sapp@us.kbr.com",
        "dale.pacwa@us.kbr.com",
        "matthew.herring@us.kbr.com",
        "sean.reese@us.kbr.com",
        "daniel.fredriksen@us.kbr.com",
        "kent.wilcher@us.kbr.com",
        "gregory.grzybowski@us.kbr.com",
        "will.casey@us.kbr.com",
        "sarah.borders@kbr.com",
        "mike.chambers@us.kbr.com",
        "jade.hong@us.kbr.com",
        "donna.vetrano@kbr.com",
        "noah.green@us.kbr.com",
        "edgardo.ortegamartinez@us.kbr.com",
        "cliff.gornto@us.kbr.com", "byron.bright@us.kbr.com", "jason.wilder@us.kbr.com", "jeff.hawks@us.kbr.com", "todd.may@us.kbr.com","reginald.hamilton@us.kbr.com","jay.lennon@us.kbr.com","scot.butkis@us.kbr.com"
    ]
    whitelist = [item.lower() for item in whitelist]

    if email.lower() in whitelist:
       return True

    raise Exception("Access Denied")

def security_check_sharepoint(dataset, token, email, client_id, oauth_secret, tenant_id):
    site = dataset["name"]
    host = dataset["host"]
    logging.info(f"Validating access to SharePoint site {site}...")      
    scope = "https://graph.microsoft.com/AllSites.Read+offline_access"
    access_token, _ = on_behalf_of(client_id, oauth_secret, tenant_id, token, scope)
    result = list_site_contents(access_token, site, host)
    if 'error' in result:
        logging.info(f"Access Denied.")
        raise Exception(result['error']['code'])
    return True

def security_check_one_drive(dataset, token, email, client_id, oauth_secret, tenant_id):
    site = dataset["id"]
    account = f"drive-{email.lower().replace('@', '-at-').replace('.', '-')}"
    logging.info(f"Validating access to OneDrive...")
    if site != account:
        raise Exception(f"Access Denied")        
    return True

SECURITY_CHECKS = {
    "azure_storage": security_check_azure,
    "SharePoint": security_check_sharepoint,
    "OneDrive": security_check_one_drive
}

def get_data_catalog(one_drive_site):

    query = {
        "query": f"SELECT * from c where c.type != 'OneDrive' or (c.type = 'OneDrive' and c.id = @onedrive_site)",
        "parameters": [{"name": "@onedrive_site", "value": one_drive_site}]
    }
    catalog, _ = query_cosmos_db(
        query,
        "metadata",
        "catalog",
    )
    return catalog

def select_dataset(email, token, client_id, oauth_secret, tenant_id, selected_datasets = None):
    onedrive_site = Ingest.convert_email_to_datasource(None, email)
    catalog = list(get_data_catalog(onedrive_site))
    datasets = []
    for dataset in catalog:
        logging.info(f"Scanning {dataset['id']}...")
        try:
            SECURITY_CHECKS[dataset["type"]](dataset, token, email, client_id, oauth_secret, tenant_id)
            datasets.append(dataset)        
            logging.info(f"Connected {dataset['id']}...")
        except Exception as ex:
            logging.info(f"Unable to connect to {dataset['id']}...")
            logging.info(ex)
            pass 

    available_dataset_ids = [dataset["id"] for dataset in datasets]

    if selected_datasets:
        if not all([dataset in available_dataset_ids for dataset in selected_datasets]):
            raise ValueError("Invalid dataset(s) selected. Please select only from the following: " + ", ".join(available_dataset_ids))
    
        datasets = [dataset for dataset in datasets if dataset["id"] in selected_datasets]

    return datasets

def list_dataset_files(email, token, client_id, oauth_secret, tenant_id, dataset_id, pagination = None, max_item_count=10, search_term = None):
    onedrive_site = Ingest.convert_email_to_datasource(None, email)
    catalog = list(get_data_catalog(onedrive_site))
    dataset = next((dataset for dataset in catalog if dataset["id"] == dataset_id), None)
    if not dataset:
        raise ValueError(f"Invalid dataset_id: {dataset_id}")
    SECURITY_CHECKS[dataset["type"]](dataset, token, email, client_id, oauth_secret, tenant_id)
    query = "SELECT * from c"
    if search_term:
        query = f"SELECT * from c where contains(c.filename, @search_term)"
    results, continuation_token = query_cosmos_db(
        query,
        "metadata",
        dataset["id"],
        continuation_token=pagination,
        max_item_count=max_item_count
    )

    #TODO Delete after adding tagging routine to ingest
    for result in results:
        result["tags"] = ["Proposal Report", "Government Contracting", "Task Order Risks", "Estimation Methodology", "Staffing Solutions", "Basis of Estimate"]

    return results, continuation_token
    