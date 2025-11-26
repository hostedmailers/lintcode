from curl_cffi import requests
import json

cookies = {
    # 'language_code': 'en',
    # 'uuid': 'db247c2a-41b2-4cc8-aa05-1c7520bb0b74',
    # '_ga': 'GA1.2.1565884597.1764100506',
    # '_gid': 'GA1.2.338777643.1764100506',
    # 'source': 'exam-re-ad',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:145.0) Gecko/20100101 Firefox/145.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'APP-VERSION': '0.0.0.1',
    'BROWSER-UUID': 'edec0a18-afbe-43f9-8c0c-49888a493325',
    # 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkX3QiOjEsImV4cCI6MTc2NDEwODA5OSwiaWF0IjoxNzY0MTA3NTk5LCJpc19sY192aWRlb19hZG1pbiI6ZmFsc2UsImlzcyI6IiIsImppdXpoYW5nX3VzZXJfaWQiOm51bGwsImp0aSI6IiIsImxpbnRjb2RlX3VzZXJfaWQiOjcwNTE1MSwic3RvcmFnZV9yb2xlIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwidXNlcl9pZCI6NzA1MTUxLCJ2ZXJzaW9uIjoxNzY0MTA3NTg4fQ.IRqbgARG8ka0-oERoEp-jDbPDaXhNcaDK9TFziRknQ0',
    # 'AcTokenTime': '1764107844069-1764108099237',
    'Origin': 'https://www.lintcode.com',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.lintcode.com/',
    # 'Cookie': 'language_code=en; uuid=db247c2a-41b2-4cc8-aa05-1c7520bb0b74; _ga=GA1.2.1565884597.1764100506; _gid=GA1.2.338777643.1764100506; source=exam-re-ad',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
}

params = {
    '_format': 'new',
    'problem_type_id': '2',
    'page_size': '200',
    'status': '4',
    'page': '1',
}

url = 'https://apiv1.lintcode.com/new/api/problems/'

all_locked_problems = []

while True:
    response = requests.get(url, params=params, cookies=cookies, headers=headers)
    print(f"Fetching {url} with params {params}")
    print(response.status_code)
    if response.status_code != 200:
        print(f"Error fetching page: {response.status_code}")
        break
    data = response.json()
    for problem in data.get('data', []):
        if problem.get('is_locked'):
            filtered = {
                'accepted_rate': problem.get('accepted_rate'),
                'en_title': problem.get('en_title'),
                'problem_id': problem.get('problem_id'),
                'is_locked': problem.get('is_locked'),
                'company_tags': problem.get('company_tags'),
                'problem_tags': problem.get('problem_tags')
            }
            all_locked_problems.append(filtered)
    if 'next' in data and data['next']:
        url = data['next']
        params = None  # next URL includes params
    else:
        break

with open('locked_problems_filtered.json', 'w') as f:
    json.dump(all_locked_problems, f, indent=4)

print(f"Collected {len(all_locked_problems)} locked problems.")