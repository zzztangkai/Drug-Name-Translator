def OCR_amazon_text(path):    
    import boto3
    # Read document content
    with open(path, 'rb') as document:
        imageBytes = bytearray(document.read())
    # Amazon Textract client
    textract = boto3.client('textract')
    # Call Amazon Textract
    response = textract.detect_document_text(Document={'Bytes': imageBytes})
    # Print detected text
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print (item["Text"])

if __name__ == "__main__":
    import sys
    OCR_amazon_text(' '.join(sys.argv[1:]))

