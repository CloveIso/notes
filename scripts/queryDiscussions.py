# -*- coding:utf-8 -*-

import argparse
import requests
from datetime import datetime
import pytz

def _make_query(owner, name, end_cursor):
    after_endCursor = ""
    if end_cursor:
        after_endCursor = 'after: "{}"'.format(end_cursor)
    query=f"""
    query {{
        repository(owner:"{owner}", name:"{name}"){{
            discussions(
                orderBy: {{field: CREATED_AT, direction: DESC}}
                first: 5
                {after_endCursor}) 
            {{
                nodes {{
                    title
                    number
                    url
                    createdAt
                    lastEditedAt
                    updatedAt
                    body
                    bodyText
                    author{{
                        login
                    }}
                    category {{
                        name
                    }}
                    labels (first: 100) {{
                        nodes {{
                            name
                        }}
                    }}
                    comments(first: 10) {{
                        nodes {{
                            body
                            author{{
                                login
                            }}
                        }}
                    }}
                }}
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
            }}
        }}
    }}
    """
    return query
    
def _request_discussions(url, headers, query):
    response = requests.post(url=url, headers=headers, json={"query": query})
    data = response.json()
    if data['data']['repository']['discussions'] is None:
        return ""
    else:
        return data['data']['repository']['discussions']

def _main():
    parser = argparse.ArgumentParser()
    parser.description = 'Query all discussions and convert it to file'
    parser.add_argument("-r", "--repo", help="GitHub repository name with namespace", dest="repo", required=True)
    parser.add_argument("-t", "--token", help="GitHub access token", dest="token", required=True)
    parser.add_argument("-o", "--output", help="Output File", dest="output", default="discussions")
    args = parser.parse_args()

    gh_repo = args.repo
    gh_token = args.token
    out_file = args.output

    gh_owner = gh_repo.split("/")[0]
    gh_repo_name = gh_repo.split("/")[-1]

    # Set request header and url
    headers = {
        "Authorization": f"Bearer {gh_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    url_graphql = "https://api.github.com/graphql"
    
    has_next_page = True
    all_discussions = []
    end_cursor = ""
    while has_next_page:
        query = _make_query(gh_owner, gh_repo_name, end_cursor)
        results = _request_discussions(url_graphql, headers, query)
        print("The value of results is:", results)
        temp_discussion = results['nodes']
        has_next_page = results['pageInfo']['hasNextPage']
        end_cursor = results['pageInfo']['endCursor']
        all_discussions.extend(temp_discussion)

    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
    discussions_with_timestamp = {'date': str(beijing_time), 'nodes': all_discussions}
    with open(out_file, "w", encoding='utf-8') as f:
        f.write(str(discussions_with_timestamp))

if __name__ == "__main__":
    _main()



