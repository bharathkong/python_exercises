
# test.py

from apicalltool import create_post

result = create_post(
    title="Python Agent",
    body="Tool Calling Demo",
    user_id=1
)

print(result)