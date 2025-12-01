import re
def text_query_to_sql(text):
    # Very simplistic natural language mapping -> return dict representing intent
    text = text.lower()
    if 'last month' in text or 'previous month' in text:
        return {'type':'expenses_last_month'}
    if 'this month' in text:
        return {'type':'expenses_this_month'}
    if 'category' in text:
        m = re.search(r'category (\w+)', text)
        return {'type':'category_query', 'category': m.group(1) if m else None}
    return {'type':'unknown', 'raw': text}

import requests
def fetch_youtube_videos(query, api_key, max_results=5):
    # Simple YouTube Data API v3 search (requires API key). Caller must set YOUTUBE_API_KEY env var.
    # Docs: https://developers.google.com/youtube/v3/docs/search/list
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part':'snippet',
        'q': query,
        'type':'video',
        'maxResults': max_results,
        'key': api_key
    }
    r = requests.get(url, params=params, timeout=10)
    if r.status_code != 200:
        return {'error': 'youtube api error', 'status': r.status_code, 'text': r.text}
    data = r.json()
    vids = []
    for it in data.get('items', []):
        vids.append({
            'title': it['snippet']['title'],
            'videoId': it['id']['videoId'],
            'description': it['snippet']['description'],
            'thumbnail': it['snippet']['thumbnails']['default']['url']
        })
    return vids
