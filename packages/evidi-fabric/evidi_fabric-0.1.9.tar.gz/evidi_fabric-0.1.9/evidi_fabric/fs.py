import pandas as pd
import sempy.fabric as fabric
import time

def get_file_path(workspace:str=None, lakehouse:str=None, directory:str=None) -> str:
    """
    Retrieves a fully qualified file path. This works independently of which lake house is active in the notebook

    Params:
     - workspace: Name of workspace (e.g. Decide_DK_DEV)
        * If not provided, the current workspace is used
     - lakehouse: Name of the lakehouse (e.g. Decide_DK_Silver)
        * If not provided, the current lakehouse is used
     - directory: Name of the directory (e.g. Bronze)

    Output:
     - path (e.g. abfss://Decide_DK_DEV@onelake.dfs.fabric.microsoft.com/Decide_DK_Silver.Lakehouse/Files/directory/
    """
    if workspace == None:
        workspace = get_workspace_name()
    if lakehouse == None:
        lakehouse = get_lakehouse_name()

    return f"abfss://{workspace}@onelake.dfs.fabric.microsoft.com/{lakehouse}.Lakehouse/Files/{directory}"


def get_table_path(table_name:str, workspace:str=None, lakehouse:str=None) -> str:
    """
    Retrieves a fully qualified table path.

    Params:
     - table_name: Name of the table (e.g. A__CUSTGROUP)
     - workspace: Name of workspace (e.g. Decide_DK_DEV)
        * If not provided, the current workspace is used
     - lakehouse: Name of the lakehouse (e.g. Decide_DK_Silver)
        * If not provided, the current lakehouse is used

    Output:
     - path (e.g. abfss://Decide_DK_DEV@onelake.dfs.fabric.microsoft.com/Decide_DK_Silver.Lakehouse/Tables/A__CUSTGROUP/
    """
    if workspace == None:
        workspace = get_workspace_name()
    if lakehouse == None:
        lakehouse = get_lakehouse_name()
    return f"abfss://{workspace}@onelake.dfs.fabric.microsoft.com/{lakehouse}.Lakehouse/Tables/{table_name}"
            
def get_lakehouse_from_path(path:str) -> str:
    """
    Retrieves the lakehouse name from a path.

    Example:
    path = "abfss://Decide_DK_DEV@onelake.dfs.fabric.microsoft.com/Decide_DK_Bronze.Lakehouse/Files/Bronze/"
    lakehouse = "Decide_DK_Bronze"
    """
    lakehouse = path.split('onelake.dfs.fabric.microsoft.com/')[-1].split('.Lakehouse')[0]
    return lakehouse

def get_workspace_id(workspace:str=None) -> str:
    """
    From the workspace name, retrieves the workspace id.
    If no workspace name is provided, the current workspace is used.
    """
    workspace=None
    if workspace == None:        
        workspace_id = fabric.get_workspace_id()
    else:
        workspace_id = fabric.resolve_workspace_id(workspace)
    return workspace_id

def get_workspace_name(workspace_id:str=None) -> str:
    """
    From the workspace id, retrieves the workspace name.
    If no workspace id is provided, the current workspace is used.
    """
    if workspace_id == None:
        workspace_id = get_workspace_id()
    
    workspace = fabric.resolve_workspace_name(workspace_id)
    return workspace


def get_lakehouse_id(lakehouse:str=None) -> str:
    """
    From the lakehouse name, retrieves the lakehouse id.
    If no lakehouse name is provided, the current lakehouse is used.
    """
    if lakehouse == None:
        lakehouse_id = fabric.get_lakehouse_id()
    else:
        df_items = fabric.list_items("Lakehouse")
        df_items = df_items[df_items['Display Name'] == lakehouse]
        lakehouse_id = df_items['Id'].iloc[0]
    return lakehouse_id

def get_lakehouse_name(lakehouse_id:str=None) -> str:
    """
    From the lakehouse id, retrieves the lakehouse name.
    If no lakehouse id is provided, the current lakehouse is used.
    """
    if lakehouse_id == None:
        lakehouse_id = get_lakehouse_id()
    
    df_items = fabric.list_items("Lakehouse")
    df_items = df_items[df_items['Id'] == lakehouse_id]
    lakehouse = df_items['Display Name'].iloc[0]
    return lakehouse

def get_lakehouse_tables(workspace_id = None, lakehouse_id = None) -> pd.DataFrame:
    """
    Retrieves the tables in the lakehouse.
    If workspace_id is not provided, the current workspace is used
    If lakehouse_id is not provided, the current lakehouse is used
    """
    if workspace_id == None:
        workspace_id = get_workspace_id()
    if lakehouse_id == None:
        lakehouse_id = get_lakehouse_id()

    workspace = get_workspace_name(workspace_id)

    client = fabric.FabricRestClient()
    response = client.get(f"/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables")
    table_list = response.json()['data']
    df_items = fabric.list_items('Lakehouse')
    df_items = df_items[df_items['Id'] == lakehouse_id]
    lakehouse = df_items['Display Name'].iloc[0]

    df = pd.DataFrame({'Workspace Name': [], 'Lakehouse Name': [], 'Table Name': [], 'Type': [], 'Location': [], 'Format': []})

    for table in table_list:
        table_name = table['name']
        table_type = table['type']
        table_location = table['location']
        table_format = table['format']

        new_data = {'Workspace Name': workspace, 'Lakehouse Name': lakehouse, 'Table Name': table_name, 'Type': table_type, 'Location': table_location, 'Format': table_format}
        df = pd.concat([df, pd.DataFrame(new_data, index=[0])], ignore_index=True)
    return df

if __name__ == "__main__":
    path="abfss://Decide_DK_DEV@onelake.dfs.fabric.microsoft.com/Decide_DK_Bronze.Lakehouse/Files/Bronze/"
    workspace="DEV"
    lakehouse=get_lakehouse_from_path(path)
    file_path=get_file_path(workspace, lakehouse, "FO_file1")

    print('Done')