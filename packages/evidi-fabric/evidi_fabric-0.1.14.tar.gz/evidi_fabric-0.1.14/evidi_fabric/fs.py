import pandas as pd
import sempy.fabric as fabric
from pyspark.sql.session import SparkSession

from evidi_fabric.spark import get_or_create_spark


def get_file_path(directory:str=None, lakehouse:str=None, workspace:str=None) -> str:
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


def get_table_path(table_name:str, lakehouse:str=None, workspace:str=None) -> str:
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

def get_lakehouse_tables_info(spark:SparkSession = None, lakehouse_id:str = None, workspace_id:str = None) -> pd.DataFrame:
    """
    Retrieves the table names and related infos from the lakehouse.
    Note: the faster method is to use the sempy API. However, due to a presumably temporary 
          pagination error, it is limited to 100 tables.
          If the number of tables equals to exactly 100, the method falls back to the spark API.
          This code should be modified (by removing the first part of the if condition) once the issue is resolved.

    If workspace_id is not provided, the current workspace is used
    If lakehouse_id is not provided, the current lakehouse is used
    """
    if workspace_id == None:
        workspace_id = get_workspace_id()
    if lakehouse_id == None:
        lakehouse_id = get_lakehouse_id()

    workspace = get_workspace_name(workspace_id)
    lakehouse = get_lakehouse_name(lakehouse_id)

    client = fabric.FabricRestClient()
    response = client.get(f"/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables")
    table_list = response.json()['data']
    if len(table_list)==100:
        warn_msg="Warning: The sempy API is truncated to show 100 tables."
        warn_msg+="\nFailing back to the spark API to retrieve all tables."
        warn_msg+="\nThis method is significantly slower."
        print(warn_msg)
        if not spark:
            spark = get_or_create_spark()
        tables = spark.catalog.listTables()
        table_list_formatted = [{"Workspace Name": workspace, 
                                 "Workspace ID": workspace_id,
                                 "Lakehouse Name": lakehouse, 
                                 "Lakehouse ID": lakehouse_id,
                                 "Table Name": table.name, 
                                 "Type":table.tableType, 
                                 "Location":None, 
                                 "Format":None, 
                                 "Is Temporary": table.isTemporary, 
                                 "Description": table.description} for table in tables]
    else:
        table_list_formatted = [{"Workspace Name": workspace, 
                                 "Workspace ID": workspace_id,
                                 "Lakehouse Name": lakehouse, 
                                 "Lakehouse ID": lakehouse_id,
                                 "Table Name": table['name'], 
                                 "Type": table['type'], 
                                 "Location": table['location'], 
                                 "Format": table['format'],
                                 "Is Temporary": None, 
                                 "Description": None} for table in table_list]
        
    return pd.DataFrame(table_list_formatted)

if __name__ == "__main__":
    path="abfss://Decide_DK_DEV@onelake.dfs.fabric.microsoft.com/Decide_DK_Bronze.Lakehouse/Files/Bronze/"
    workspace="DEV"
    lakehouse=get_lakehouse_from_path(path)
    file_path=get_file_path(workspace, lakehouse, "FO_file1")

    print('Done')