import time

def get_file_path(workspace:str, lakehouse:str, directory:str=None) -> str:
    """
    Retrieves a fully qualified file path. This works independently of which lake house is active in the notebook

    Params:
     - workspace: Name of workspace (e.g. Decide_DK_DEV)
     - lakehouse: Name of the lakehouse (e.g. Decide_DK_Silver)
     - directory: Name of the directory (e.g. Bronze)

    Output:
     - path (e.g. abfss://Decide_DK_DEV@onelake.dfs.fabric.microsoft.com/Decide_DK_Silver.Lakehouse/Files/directory/
    """
    return f"abfss://{workspace}@onelake.dfs.fabric.microsoft.com/{lakehouse}.Lakehouse/Files/{directory}"


def get_table_path(lakehouse:str, table_name:str, max_attempts:int=10) -> str:
    """
    Retrieves a fully qualified table path. This works independently of which lake house is active in the notebook

    Params:
     - lakehouse: Name of the lakehouse (e.g. Decide_DK_Silver)
     - table_name: Name of the table (e.g. A__CUSTGROUP)

    Output:
     - path (e.g. abfss://Decide_DK_DEV@onelake.dfs.fabric.microsoft.com/Decide_DK_Silver.Lakehouse/Tables/A__CUSTGROUP/
    """
    attempt=1
    while True:
        try:
            return f"{mssparkutils.lakehouse.get(lakehouse).abfsPath}/Tables/{table_name}"
        except Exception as e:
            if attempt<max_attempts:
                print(f"Failed to retrieve table path, for table {table_name}. Waiting 10 seconds and continue with attempt: {attempt+1}")
                time.sleep(10)
                attempt+=1
            else:
                err_str=f"Failed to retrieve table path, for table {table_name}, due to the following reason\n"
                err_str+=str(e)
                raise RuntimeError(err_str)
            
def get_lakehouse_from_path(path:str) -> str:
    """
    Retrieves the lakehouse name from a path.

    Example:
    path = "abfss://Decide_DK_DEV@onelake.dfs.fabric.microsoft.com/Decide_DK_Bronze.Lakehouse/Files/Bronze/"
    lakehouse = "Decide_DK_Bronze"
    """
    lakehouse = path.split('onelake.dfs.fabric.microsoft.com/')[-1].split('.Lakehouse')[0]
    return lakehouse

if __name__ == "__main__":
    path="abfss://Decide_DK_DEV@onelake.dfs.fabric.microsoft.com/Decide_DK_Bronze.Lakehouse/Files/Bronze/"
    workspace="DEV"
    lakehouse=get_lakehouse_from_path(path)
    file_path=get_file_path(workspace, lakehouse, "FO_file1")

    print('Done')