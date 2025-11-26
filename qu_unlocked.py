import json
import concurrent.futures
import logging
import time
from curl_cffi import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

cookies = {
    'language_code': 'en',
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
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkX3QiOjEsImV4cCI6MTc2NDEwOTQzOCwiaWF0IjoxNzY0MTA4OTM4LCJpc19sY192aWRlb19hZG1pbiI6ZmFsc2UsImlzcyI6IiIsImppdXpoYW5nX3VzZXJfaWQiOm51bGwsImp0aSI6IiIsImxpbnRjb2RlX3VzZXJfaWQiOjcwNTE1MSwic3RvcmFnZV9yb2xlIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwidXNlcl9pZCI6NzA1MTUxLCJ2ZXJzaW9uIjoxNzY0MTA3NTg4fQ.VUPqLQeCqtNSk0Zg2dfIWA1IjqJdQRyIDXXGdVpThqQ',
    # 'AcTokenTime': '1764108939777-1764109438030',
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
    'lang': '2',
}

def fetch_problem_detail(problem_id):
    logging.info(f"Starting fetch for problem_id {problem_id}")
    url = f'https://apiv1.lintcode.com/v2/api/problems/{problem_id}/'
    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, params=params, cookies=cookies, headers=headers)
        except Exception as exc:
            logging.error(f"Request error for {problem_id} on attempt {attempt}: {exc}")
            if attempt == max_attempts:
                return False, None
            continue

        if response.status_code == 200:
            logging.info(f"Successfully fetched problem_id {problem_id}")
            time.sleep(0.5)  # Gentle rate limit between successes
            return True, response.json()

        if response.status_code == 429:
            logging.warning(f"Rate limited on problem_id {problem_id} (attempt {attempt}), retrying in 3s")
            if attempt == max_attempts:
                return False, None
            time.sleep(3)
            continue

        logging.error(f"Failed to fetch {problem_id}: {response.status_code} on attempt {attempt}")
        if attempt == max_attempts:
            return False, None

    return False, None

# Load all problems and grab every problem id
with open('all_problems.json', 'r') as f:
    problems = json.load(f)

problem_ids = [p['problem_id'] for p in problems if 'problem_id' in p]

print(f"Fetching details for {len(problem_ids)} problems...")

results = []
failed_ids = []
retry_queue = problem_ids[:]
attempt_round = 1

while retry_queue:
    logging.info(f"Starting round {attempt_round} with {len(retry_queue)} IDs")
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        futures = {executor.submit(fetch_problem_detail, pid): pid for pid in retry_queue}
        retry_queue = []
        for future in concurrent.futures.as_completed(futures):
            pid = futures[future]
            try:
                success, data = future.result()
                if success and data:
                    results.append(data)
                    with open('all_question_details_unlocked.json', 'w') as f:
                        json.dump(results, f, indent=4)
                else:
                    retry_queue.append(pid)
            except Exception as exc:
                logging.error(f'{pid} generated an exception: {exc}')
                retry_queue.append(pid)

    attempt_round += 1
    if attempt_round > 25:  # avoid infinite loops
        failed_ids.extend(retry_queue)
        break

if failed_ids:
    logging.warning(f"Failed to fetch {len(failed_ids)} problems after retries")
    with open('failed_problem_ids.json', 'w') as f:
        json.dump(failed_ids, f, indent=2)
else:
    logging.info("Fetched details for all problems")

logging.info(f"Final count: Collected details for {len(results)} problems.")