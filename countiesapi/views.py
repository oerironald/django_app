import requests
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import json

def fetch_counties(request):
    url = 'https://vickie-demo-server.onrender.com/api/counties'
    headers = {
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        counties = response.json()  # Parse the JSON response
        return render(request, 'countiesapi/county_list.html', {'counties': counties, 'current_year': datetime.now().year})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)


BASE_URL = "https://kenya-api.onrender.com"

def health_check(request):
    response = requests.get(f"{BASE_URL}/health")
    return JsonResponse(response.json())

def get_countries(request):
    try:
        # Fetch data from the external API
        response = requests.get(f"{BASE_URL}/country")
        print("Response Status Code:", response.status_code)  # Debugging line
        
        if response.status_code == 200:
            country_info = response.json().get('countryInfo', {}).get('0', {})
            print("Fetched Data:", country_info)  # Debugging line

            # Prepare data for template
            country_info['official_languages'] = country_info.pop('official-languages', [])
            country_info['driving_side'] = country_info.pop('driving-side', '')
            country_info['calling_code'] = country_info.pop('caling-code', '')  # Note the typo
            country_info['ISO_3166_code'] = country_info.pop('ISO-3166-code', '')
            country_info['president_image'] = country_info.pop('president-image', '')

            return render(request, 'kenya_api/index.html', {'country_info': country_info})
        else:
            print("Error fetching data from API:", response.status_code)  # Debugging line
            return render(request, 'countiesapi/countries.html', {'error': 'Failed to fetch data from API.'})
    except Exception as e:
        print("Exception occurred:", str(e))  # Debugging line
        return render(request, 'countiesapi/countries.html', {'error': 'An error occurred.'})
    
def get_counties(request):
    response = requests.get(f"{BASE_URL}/county")
    counties = response.json()
    return render(request, 'countiesapi/counties.html', {'counties': counties})

def get_wards(request):
    response = requests.get(f"{BASE_URL}/wards")
    wards = response.json()
    return render(request, 'countiesapi/wards.html', {'wards': wards})

def get_postal_stations(request):
    response = requests.get(f"{BASE_URL}/postal_stations")
    postal_stations = response.json()
    return render(request, 'countiesapi/postal_stations.html', {'postal_stations': postal_stations})





def country_info(request):
    api_url = "https://kenya-api.onrender.com/country"  # Your actual API URL
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Ensure the response status is OK (200)
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return render(request, 'countiesapi/country_info.html', {'error': 'Failed to fetch data from the API.'})

    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))  # Print data to Django console for inspection
        country_info = data.get('countryInfo', {}).get('0', {})
        
        # Handle hyphenated keys
        country_info['president_image'] = country_info.get('president-image')
        country_info['time_zone'] = country_info.get('time-Zone')
        country_info['driving_side'] = country_info.get('driving-side')
    else:
        country_info = {}

    return render(request, 'countiesapi/country_info.html', {'country_info': country_info})