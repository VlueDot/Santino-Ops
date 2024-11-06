import time
from firebase_admin import firestore

db = firestore.client()

def log_api_usage(company_id, service, api_type, data_size, processing_time):
    log_ref = db.collection("metrics").document(company_id).collection("usage_logs").document()
    log_ref.set({
        "timestamp": firestore.SERVER_TIMESTAMP,
        "service": service,
        "api_type": api_type,
        "data_size": data_size,
        "processing_time": processing_time,
    })

def track_function_usage(company_id, function_name):
    start_time = time.time()
    
    # Ejemplo de función que se está rastreando
    # ... Ejecución de la función ...
    
    end_time = time.time()
    processing_time = end_time - start_time
    log_api_usage(company_id, function_name, "firebase_function", None, processing_time)