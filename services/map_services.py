import requests

def get_address_details(address_text, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?language=en&address={address_text}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if not data.get('results'):
        return None
        
    result = data['results'][0]
    components = result.get('address_components', [])
    
    types = [c['types'][0] for c in components if c.get('types')]
    
    return {
        'formatted_address': result.get('formatted_address'),
        'is_route': 'route' in types,
        'is_street_number': 'street_number' in types,
        'lat': result['geometry']['location']['lat'],
        'lng': result['geometry']['location']['lng'],
        # city or country
        'city_name': components[4]['long_name'] if len(components) > 4 else '0'
    }