import os
from typing import Optional


def delete_dataset_file(path: Optional[str]) -> None:
    """
    Deletes a dataset locally using its path from the database
    """
    if os.path.exists(path):
        try:
            os.remove(path)
            return
        except Exception as ex:
            raise OSError(f"Its impossible to delete file: [{path}] \n {ex}")
    else:
        raise FileNotFoundError("File not found")








