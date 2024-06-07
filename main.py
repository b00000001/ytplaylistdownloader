import os
import io

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    def get_all_playlist_items(playlist_id):
        playlist_items = []
        next_page_token = None
        while True:
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                maxResults=50,
                playlistId=playlist_id,
                pageToken=next_page_token,
        )
            response = request.execute()
            playlist_items.extend(response["items"])
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        return playlist_items
    
    playlist_items = get_all_playlist_items("PLB371676A96E8C406")
    
    with open("playlist_items.txt", "w", encoding="utf-8") as f:
        print(type(playlist_items))
        for item in playlist_items:                        
                         if(item['snippet']['title'] == 'Deleted video') or (item['snippet']['title'] == 'Private video'):
                             pass
                         else:
                             f.write(f"{item['snippet']['title']}  - {str(item['snippet']['videoOwnerChannelTitle'])}\n")
                         
if __name__ == "__main__":
    main()