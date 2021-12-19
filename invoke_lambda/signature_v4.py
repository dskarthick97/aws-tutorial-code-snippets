"""
Signature Version 4 Module
"""

import datetime
import hashlib
import hmac

import requests

# request values
method = 'GET'
service = 'execute-api'
host = 'joi78jigv6.execute-api.ap-south-1.amazonaws.com'
region = 'ap-south-1'
endpoint = 'https://joi78jigv6.execute-api.ap-south-1.amazonaws.com'
request_parameters = ''


def sign(key, message):
    return hmac.new(key, message.encode('utf-8'), hashlib.sha256).digest()


def get_signature_key(key, date_stamp, region_name, service_name):
    date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    region = sign(date, region_name)
    service = sign(region, service_name)
    signing_key = sign(service, 'aws4_request')
    return signing_key


# access_key = os.environ.get('AWS_ACCESS_KEY_ID')
# secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
# if access_key or secret_key is None:
#     print('No access key is available')
#     sys.exit()

t = datetime.datetime.utcnow()
amzdate = t.strftime('%Y%m%dT%H%M%SZ')
datestamp = t.strftime('%Y%m%d')

# Task 1: CREATE A CANONICAL REQUEST

# Step 1: Define the action -- already done

# Step 2: Create a canonical URI -- the part of the URI from domain to query
# string. use '/' if no path
canonical_uri = '/dev'

# Step 3: Create a canonical query string. It should be url-encoded
# use empty string('') if no query params
canonical_querystring = request_parameters

# Step 4: Create the canonical headers. The canonical headers consists of a
# list of all the HTTP headers that are included with the signed request
canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'

# Step 5: Create a signed headers. The value is the list of headers that are
# included in the canonical headers
signed_headers = 'host;x-amz-date'

# Step 6: Create payload hash (hash of the request body content). For GET
# requests, the payload is an empty string ('')
payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()

# Step 7: Combine elements to create canonical request
canonical_request = '\n'.join((method, canonical_uri, canonical_querystring,
                               canonical_headers, signed_headers, payload_hash))

# Step 8: Create a digest(hash) of the canonical request with the same
# algorithm that used to hash the payload
canonical_request_digest = hashlib.sha256(
    canonical_request.encode('utf-8')).hexdigest()


# Task 2: CREATE A STRING TO SIGN

# Step 9: Algorithm designation
algorithm = 'AWS4-HMAC-SHA256'

# Step 10: Create a credential scope. The value is a string that includes the
# date, region, service and a termination string('aws4_request')
credential_scope = '/'.join((datestamp, region, service, 'aws4_request'))

# Step 11: Create a string to sign by appending algorithm, request_date,
# credential_scope and canonical_request_ digest
string_to_sign = '\n'.join((algorithm, amzdate, credential_scope,
                            canonical_request_digest))


# Task 3: CALCULATE THE SIGNATURE

# Step 12: Create a signing key using the function defined above
signing_key = get_signature_key(secret_key, datestamp, region, service)

# Step 13: Sign the string_to_sign using the signing_key
signature = hmac.new(signing_key, string_to_sign.encode('utf-8'),
                     hashlib.sha256).hexdigest()


# Task 4: ADD SIGNING INFORMATION TO THE REQUEST

# Step 14: Create the authorization header and add to the request header
credential = '/'.join((access_key, credential_scope))
authorization_header = algorithm + ' ' + 'Credential=' + credential + \
    ', ' + 'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + \
    signature

headers = {'x-amz-date': amzdate, 'Authorization': authorization_header}

# # Step 15: Send the request
request_url = endpoint + canonical_uri
r = requests.get(request_url, headers=headers)
print('Status Code: {}'.format(r.status_code))
print('Text: {}'.format(r.text))
