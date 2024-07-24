import os
import sys
import json
from dotenv import load_dotenv
import ovh

# Load environment variables from .env file
load_dotenv()

if len(sys.argv) != 5:
    print(f"Usage: python3 {sys.argv[0]}) <zone_domain_name> <sub_domain_name> <record_id> <public_ip>")
    sys.exit(1)

zone_name = sys.argv[1]
sub = sys.argv[2]
record_id = sys.argv[3]
public_ip = sys.argv[4]

# Retrieve values from environment variables
application_key = os.getenv('OVH_APPLICATION_KEY')
application_secret = os.getenv('OVH_APPLICATION_SECRET')
consumer_key = os.getenv('OVH_CONSUMER_KEY')
#zone_name='<zone_name>'
#sub='<subdomain>'
subdomain=f'{sub}.{zone_name}'
#record_id='<5315708482>'
#public_ip='<public_ip>'
# OVH API endpoint
ovh_endpoint = 'ovh-eu'
# Initialize OVH client
client = ovh.Client(
endpoint=ovh_endpoint,
application_key=application_key,
application_secret=application_secret,
consumer_key=consumer_key
)

print(f'Fetching record for {subdomain}')
result = client.get(f'/domain/zone/{zone_name}/record/{record_id}')
print(result)
print(f'Updating target record for {subdomain}')
print(f'Public IP = {public_ip}')
result = client.put(f'/domain/zone/{zone_name}/record/{record_id}',
fieldType='A',
subDomain=sub,
target=public_ip,
ttl=60
)
# print(result)
print(f'Refreshing zone {zone_name}')
result = client.post(f'/domain/zone/{zone_name}/refresh')
# print(result)
