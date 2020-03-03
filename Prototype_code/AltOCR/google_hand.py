def OCR_google_hand(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    import os
    #Sets enviroment variable to json path
    credential_path = "/home/jamal/OCRCapstone.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    #Creates a imageAnnotator object (part of Google vision)
    client = vision.ImageAnnotatorClient()
    #Open image as byte array
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    #Basically an abstracted POST request using the google.cloud module,
    #and sends the image
    image = vision.types.Image(content=content)
    #Capture response of Google Vision's Document Text Detection
    response = client.document_text_detection(image=image)
    #Extracts only the text
    texts = response.text_annotations
    print(texts[0].description)


if __name__ == "__main__":
    import sys
    OCR_google_hand(' '.join(sys.argv[1:]))

