import requests
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime

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