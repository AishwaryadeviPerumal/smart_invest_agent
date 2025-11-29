import os
import sys
print(sys.path)
from jproperties import Properties

props = Properties()
with open('../properties/app-config.properties', 'rb') as props_file:
    props.load(props_file)
google_api_key = props.get('GOOGLE_API_KEY').data
os.environ["GOOGLE_API_KEY"] = google_api_key