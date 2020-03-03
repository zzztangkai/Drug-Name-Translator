def OCR_azure_text(path):
    import requests
    import os
    import sys
    #hardcoded keys for testings, these will be pulled from 
    #the enviroment variable later on
    subscription_key = os.environ['AZURE_KEY'] 
    #subscription_key = "cd741d49ceb046ae842c5a425b70af57"
    endpoint ="https://westcentralus.api.cognitive.microsoft.com/"
    ocr_url = endpoint + "vision/v2.0/ocr"

    # Read the image into a byte array
    image_data = open(path, "rb").read()
    # Setting headers to make request to REST API, these are
    #the API key, endpoint and content type
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    #Parameters tell the API what lang to look for
    params = {'language': 'en', 'detectOrientation': 'true'}

    #Post request to the API with headers, params and image data stream
    response = requests.post(ocr_url, headers=headers, params=params, data = image_data)
    #checks for status codes returns by the API 
    response.raise_for_status()
    #Converts the reposnse object into a json file
    analysis = response.json()

    # Extract the word bounding blocks and text.
    line_infos = [region["lines"] for region in analysis["regions"]]
    word_infos = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                word_infos.append(word_info)
    #Extracts the raw text from the bounding blocks
    text = []
    for word in word_infos:
        text.append(word["text"])
    print(text)

if __name__ == "__main__":
    import sys
    OCR_azure_text(' '.join(sys.argv[1:]))

