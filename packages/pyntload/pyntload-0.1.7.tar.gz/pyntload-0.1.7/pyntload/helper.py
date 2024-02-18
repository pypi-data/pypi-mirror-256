import requests
import base64
import json
import sys,imp

#headers to use
headers = {
        "Accept": "application/json,text/javascript,*/*",
        'Authorization': 'Bearer dapi03fa57be956e3d0a07a050177327334d-2',
        "Content-Type": "application/json"
}

#base url
base_url = "https://adb-7118152657858843.3.azuredatabricks.net/"

def read_databricks_notebook(notebook_path):
        
    #get notebook export
    response = requests.request(
        "GET",
        base_url + "api/2.0/workspace/export",
        headers =headers,
        params= {
            'path': notebook_path,
            'format': 'JUPYTER'
        }
    )
    
    #parse python code (json to dict)
    jupyter_code = json.loads(base64.b64decode(response.json()["content"]))
    jupyter_code_cells = [cell for cell in jupyter_code["cells"] if cell["cell_type"]=="code"]
    #jupyter_code_cells = [''.join(cell['source']) for cell in jupyter_code_cells]
        
    return jupyter_code_cells
