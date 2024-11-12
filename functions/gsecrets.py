from google.cloud import secretmanager

import os



# cred = credentials.Certificate("santino-ops-firebase-adminsdk-t43d5-86eab65852.json")
# firebase_admin.initialize_app(cred)


def access_secret(secret_name, project_id=os.getenv("GCLOUD_PROJECT")):
    """
    Accede al valor de un secreto en Google Secret Manager.
    :param secret_name: Nombre del secreto en Google Secret Manager.
    :param project_id: ID del proyecto de Google Cloud.
    :return: Valor del secreto como una cadena de texto.
    """
    
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def list_secrets(project_id=os.getenv("GCLOUD_PROJECT")):
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"

    for secret in client.list_secrets(request={"parent": parent}):
        print(f"Found secret: {secret.name}")


