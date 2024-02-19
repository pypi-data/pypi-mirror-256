import requests
import json

GRAPH_URL = "https://graph.microsoft.com/v1.0/"

def on_behalf_of(client_id, client_secret, tenant_id, assertion_token, scope):
    AUTH_URL = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    
    grant_type = "urn:ietf:params:oauth:grant-type:jwt-bearer"
    query_params = f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&assertion={assertion_token}&scope={scope}&requested_token_use=on_behalf_of"
    response = requests.post(AUTH_URL, data=f"{query_params}", headers={"Content-Type": "application/x-www-form-urlencoded"})
    token_data = response.json()
    if 'access_token' not in token_data:
        raise ValueError(f"On Behalf of request failed: {token_data}")
    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]
    
    return access_token, refresh_token

def list_site_contents(access_token, site, host):
    HEADERS = {'Authorization': f"Bearer {access_token}" }        
    response = requests.get(f"{GRAPH_URL}sites/{host}:/sites/{site}:/drives", headers=HEADERS) 
    return json.loads(response.text)
