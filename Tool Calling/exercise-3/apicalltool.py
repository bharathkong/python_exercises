import requests

def create_post(
        title: str,
        body: str,
        user_id: int
) -> str:
    """
    Create a sample post.
    """

    payload = {
        "title": "Sample POST by KBK",
        "body": "sample body by kbk",
        "userId": 10001
    }

    response = requests.post(
        "https://jsonplaceholder.typicode.com/posts",
        json=payload
    )

    print(response)
    return response.text