from googleapiclient.discovery import build


def fetch_comments(id: str, max_result=2000, max_len=200) -> list[str]:
    """
    Fetches comments from a youtube video.
    :param id: The id of the video.
    :param max_cout: The maximum number of comments to fetch.
    :return: A list of comments.
    """

    youtube = build('youtube', 'v3', developerKey='AIzaSyDJfkTXmC0nbuCAn4_NWpCmgrCFHw4DE_E')

    all_comments = []

    next_page_token = None
    while True:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=id,
            pageToken=next_page_token,
            maxResults=1000,  # Maximum allowed
            textFormat='plainText'
        ).execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comment = comment[:max_len]
            all_comments.append(comment)

        if len(all_comments) > max_result:
            break

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    return all_comments