from google.cloud import firestore
from constants import UserState
from datetime import datetime

import time

db = firestore.Client()

def set_user_state(user_id: str, state: UserState):
    user_ref = db.collection('users').document(user_id)
    user_ref.update({'state': state.value})

def get_user_data(user_id: str):
    user_ref = db.collection('users').document(user_id)
    doc = user_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None

def get_user_reports(user_id: str):
    reports_ref = db.collection('bikereport')
    query = reports_ref.where('user_id', '==', user_id).stream()
    
    return [doc.to_dict() for doc in query]

def get_report_by_timestamp(user_id: str, timestamp: str):
    reports_ref = db.collection('bikereport')

    query = reports_ref.where('user_id', '==', user_id)\
                       .where('timestampz', '==', timestamp)\
                       .limit(1).get()
    
    return query[0].to_dict() if query else None

def execute_report_abandonment(user_id, timestamp, current_total):
    batch = db.batch()
    
    # find report
    reports_ref = db.collection('bikereport')
    query = reports_ref.where('user_id', '==', user_id)\
                       .where('timestampz', '==', timestamp)\
                       .limit(1).get()
    
    if not query:
        return False

    report_doc = query[0]
    report_data = report_doc.to_dict()

    # write into backup (bikereportbackup)
    backup_ref = db.collection('bikereportbackup').document(report_doc.id)
    batch.set(backup_ref, report_data)

    # delete (bikereport)
    batch.delete(report_doc.reference)

    # update user report count (totalz - 1)
    user_ref = db.collection('users').document(user_id)
    batch.update(user_ref, {
        'state': UserState.MENU,           
        'totalz': max(0, current_total - 1)
    })

    batch.commit()
    return True


def initialize_user(user_id: str):
    default_data = {
        'user_id': user_id,
        'name': "<empty>",
        'pnum': "<empty>",
        'state':0,
        'picture':0,
        'correct':-1,
        'newclient':1,
        'credit':"0.0", 
        'totalz':0,
        'consecution':0,
        'localz':0,
        'score':0
    }

    db.collection('users').document(user_id).set(default_data)

    return default_data

def submit_final_report(user_id, user_data, final_credit):
    batch = db.batch()
    now = datetime.now()
    
    # create bikereport
    report_ref = db.collection('bikereport').document()
    report_data = {
        'rid': int(time.mktime(now.timetuple())),
        'timestampz': str(now),
        'user_id': user_id,
        'namez': user_data.get('namez'),
        'pnum': user_data.get('pnum'),
        'bikephoto': user_data.get('urlz'),
        'address': user_data.get('address'),
        'score': user_data.get('score'),
        'status': "reported",
        'updatedate': str(now),
        'details': user_data.get('details', "-")
    }
    batch.set(report_ref, report_data)

    # update user report count
    user_ref = db.collection('users').document(user_id)
    batch.update(user_ref, {
        'state': UserState.MENU,
        'score': 0,                   
        'credit': str(final_credit),  
        'totalz': int(user_data.get('totalz', 0)) + 1, 
        'picture': 0,                 
        'correct': -1                 
    })

    batch.commit()
    return True

def update_report_score_state(user_id, score, address, lat = 0, lng = 0):
    user_ref = db.collection('users').document(user_id)
    
    update_data = {
        'state': UserState.CONFIRMING_REPORT,
        'score': int(score), 
        'address': address,
        'latz': str(lat), 
        'longz': str(lng),
        'localz': 2
    }

    user_ref.update(update_data)
    return True

def update_user_name_and_check_state(user_id, new_name, current_phone):
    user_ref = db.collection('users').document(user_id)
    
    if new_name == '<empty>' or current_phone == '<empty>':
        next_state = UserState.MENU
    else:
        next_state = UserState.WAITING_FOR_PHOTO
        
    user_ref.update({
        'namez': new_name,
        'state': next_state
    })
    
    return next_state

def update_user_phone_and_check_state(user_id, new_phone, current_name):
    user_ref = db.collection('users').document(user_id)
    
    if new_phone == '<empty>' or current_name == '<empty>':
        next_state = UserState.MENU
    else:
        next_state = UserState.WAITING_FOR_PHOTO
        
    user_ref.update({
        'pnum': new_phone,
        'state': next_state
    })
    return next_state

def update_user_temp_address(user_id, address):
    user_ref = db.collection('users').document(user_id)
    user_ref.update({
        'address': address,
        'latz': '0',
        'longz': '0',
        'details': '-',
        'email': '0'
    })

def update_user_location_details(user_id, detail_text):
    user_ref = db.collection('users').document(user_id)
    user_ref.update({
        'details': detail_text,
        'state': UserState.WAITING_FOR_DETAILS
    })
    return True    

def update_user_photo_result(user_id, photo_url, has_bike):
    # update photo_url
    user_ref = db.collection('users').document(user_id)
    
    is_correct = 1 if has_bike else 0
    
    update_data = {
        'urlz': photo_url,                   
        'picture': 1,                        
        'correct': is_correct,              
        'state': UserState.ADDRESS_CONFIRMATION
    }
    
    user_ref.update(update_data)
    return True