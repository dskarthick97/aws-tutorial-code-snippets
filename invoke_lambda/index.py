import hashlib

from aws_request_signer import AwsRequestSigner
import requests


def main():
    AWS_REGION = 'ap-south-1'
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    URL = 'https://joi78jigv6.execute-api.ap-south-1.amazonaws.com/dev'
    service = 'execute-api'

    content = ''.encode('utf-8')
    content_hash = hashlib.sha256(content).hexdigest()

    request_signer = AwsRequestSigner(
        AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, service)

    headers = {
        'Content-Type': 'application/json',
        'Content-Length': str(len(content))
    }

    headers.update(request_signer.sign_with_headers(
        'GET', URL, headers, content_hash))

    response = requests.get(URL, headers=headers, data=content)
    print('Text: {}'.format(response.text))


if __name__ == '__main__':
    main()
