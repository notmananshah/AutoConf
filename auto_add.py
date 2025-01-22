#!/usr/bin/env python3

import os
import requests

def main():
    servers = []

    print("Enter the server names you want to add to the inventory file. Enter them one by one. Type 'exit()' to exit.\n")
    while True:
        server_name = input("> ")
        if server_name.strip().lower() == "exit()":
            break

        # Skips empty lines
        if not server_name.strip():
            continue
        servers.append(server_name.strip())

    # If no servers were added, exit
    if not servers:
        print("No servers added. Exiting without updating Confluence.")
        return
    
    # CONFLUENCE SETUP
    full_page_url = "https://notmananshah.atlassian.net/wiki/spaces/CT/pages/360453/Automation+Testing"
    base_url = "https://notmananshah.atlassian.net/wiki/rest/api"
    page_id = "360453"
    space_key = "CT"
    username = "manan.jshah@yahoo.com"

    # Read API token from environment variable
    api_token = os.environ.get("CONFLUENCE_API_TOKEN")
    if not api_token:
        print("API token not found. Exiting without updating Confluence.")
        return
    
    # Get the page content
    url_get = f"{base_url}/content/{page_id}?expand=body.storage,version"
    auth = (username, api_token)

    response = requests.get(url_get, auth=auth)
    if response.status_code != 200:
        print(f"Failed to get page content. Status code: {response.status_code}")
        return
    
    page_data = response.json()
    current_version = page_data["version"]["number"]
    current_title = page_data["title"]
    current_body = page_data["body"]["storage"]["value"]

    # Update the page content
    new_body = current_body + "\n" 
    for server in servers:
        new_body += f"<p>{server}</p>\n"

    # Update the page
    url_put = f"{base_url}/content/{page_id}"
    headers = {"Content-Type": "application/json"}

    payload = {
        "id": page_id,
        "type": "page",
        "title": current_title,
        "space": {"key": space_key},
        "body": {"storage": {"value": new_body, "representation": "storage"}},
        "version": {"number": current_version + 1}
    }

    update_response = requests.put(url_put, headers=headers, json=payload, auth=auth)

    if update_response.status_code == 200:
        print(f"Successfully updated the page with the following servers: ")
        for s in servers:
            print(f" - {s}")
    else:
        print(f"Failed to update the page. Status code: {update_response.status_code}")

if __name__ == "__main__":
    main()