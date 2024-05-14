from requests import get from xml.etree import ElementTree as ET import pandas as pd

url = 'https://data.cityofnewyork.us/api/odata/v4/k397-673e/$metadata' # Replace with the correct url for the XML data response = get(url)

if response.status_code == 200: xml_data = response.text else: print('Failed to get data:', response.status_code) exit(1)

root = ET.fromstring(xml_data)

field_names = [ f'{field.attrib["name"]}' for field in root.findall(".//{https://data.cityofnewyork.us/api/odata/v4/k397-673e/$metadata}Property", root.nsmap) ]

records = [] for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry", root.nsmap): record = {} for prop in entry.findall(".//{http://schemas.microsoft.com/ado/2009/02/edm}properties"): for child in prop: if child.tag.endswith('type="Decimal"'): value = float(child.text) elif child.tag.endswith('null="true"'): value = None else: value = child.text record[child.tag.split('}')[-1]] = value records.append(record)
df = pd.DataFrame(records)
df.columns = [field_name.replace('_', ' ').title() for field_name in df.columns]
print(df.head())


"""
 In the code above, the XML data is fetched from the specified URL using the requests library. The XML data is then parsed using the xml.etree.ElementTree library. 
The field names are extracted from the XML data by finding all elements with the tag "{https://data.cityofnewyork.us/api/odata/v4/k397-673e/$metadataProperty". 
The data from the XML data is extracted by iterating over each entry element in the XML data. The record dictionary is then appended to the records list. Finally, 
the extracted data is converted to a pandas DataFrame and displayed.

"""