# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`


from firebase_functions import https_fn
from firebase_admin import initialize_app
from flask import Flask

from gsecrets import access_secret, list_secrets
from services import gmail
from services.ia import talk_ai, deliver_tasks
from services_management.management import get_company_from_mail



initialize_app()
app = Flask(__name__)


# ________________________________________________________________

@app.route("/read_incomming_mails")
def read_incomming_mails():
    try:
        # load_emails_company_tasks() # get access,emails to check, 
        
        company = "AirSeaLogistics"
        secret_value = access_secret("gmail_app_password")
        mails = gmail.read_emails(secret_value)
        response = []
        for mail in mails:
            response.append (deliver_tasks( company, mail) )# hilos independientes para mail y compania
            
        
            

        





        return {"mails": mails, "response" : response} 
    except Exception as e:
        return f"Error accessing : {e}"











@app.route("/secrets")
def secrets_test():
    try:
        list_secrets()
        secret_value = access_secret("Outlook_mailAPI_tenantID")
        return f"Secret Value: {secret_value}"
    except Exception as e:
        return f"Error accessing secret: {e}"


# ________________________________________________________________




# Para que funcione como función de Firebase
@https_fn.on_request()
def santino_ops(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):

        return app.full_dispatch_request()
    

if __name__ == '__main__':

    app.run(debug=True)


@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    return https_fn.Response("Hello world!")