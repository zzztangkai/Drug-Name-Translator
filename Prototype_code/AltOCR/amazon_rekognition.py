def OCR_amazon_hand(path):    
    import boto3
    # Read document content
    with open(path, 'rb') as document:
        imageBytes = bytearray(document.read())
    # Amazon rekognition client
    textract = boto3.client('rekognition')
    # Call Amazon Textract
    response = textract.detect_text(Image={'Bytes': imageBytes})
    # Print detected text
    for item in response["TextDetections"]:
        if item["Type"] == "LINE":
            print (item["DetectedText"])

if __name__ == "__main__":
    import sys
    detect_text_amazon(' '.join(sys.argv[1:]))

