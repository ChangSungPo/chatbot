import os
import requests
from google.cloud import vision
from google.protobuf.json_format import MessageToJson, MessageToDict

vision_client = vision.ImageAnnotatorClient()

def detect_bicycle_in_image(image_uri, keyword = "bicycle"):

    try:
        download_response = requests.get(image_uri)
        if download_response.status_code != 200:
            print(f"Error downloading image: {download_response.status_code}")
            return False
        content = download_response.content
    except Exception as e:
        print(f"Download failed: {e}")
        return False
    
    image = vision.Image(content=content)

    try:
        response = vision_client.label_detection(image=image)
        labels = response.label_annotations
        has_keyword = any(keyword.lower() in label.description.lower() for label in labels)
        
        if response.error.message:
            print(f"Vision API Error: {response.error.message}")
            return False
        
        if labels:
            print(f"DEBUG - Labels found: {[l.description for l in labels]}")
            
        return has_keyword
    except Exception as e:
        print(f"Error during label detection: {e}")
        return False

def recognize_doorplate_text(image_uri):
    # download photo
    try:
        response = requests.get(image_uri)
        if response.status_code != 200:
            print(f"ERROR - unable to download photo: {response.status_code}")
            return None
        content = response.content
    except Exception as e:
        print(f"ERROR - download error: {e}")
        return None

    image = vision.Image(content=content)
    # image.source.image_uri = image_uri
  
    try:
        response = vision_client.document_text_detection(image=image)
        response_dict = MessageToDict(response._pb)
        print(f"DEBUG - Vision Response: {response_dict}")
        if response.text_annotations:
            full_text = response.text_annotations[0].description
            return ",".join(full_text.split()) 
        return None

    except Exception as e:
        print(f"Error during text detection: {e}")
        return None