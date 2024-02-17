import json
import io

def get_json(gcloud_path, storage_client):
    """
    Args:
        gcloud_path (str): path en google cloud storage
        storage_client (Client): cliente de google cloud storage

    Returns:
        dict: json con la data del archivo
    """
    # Creamos un archivo temporal que holdea la data del archivo en gcloud_path
    tmp_file = io.BytesIO()
    storage_client.download_blob_to_file(gcloud_path, tmp_file)
    tmp_file.seek(0)
    
    data = json.load(tmp_file)
        
    return data