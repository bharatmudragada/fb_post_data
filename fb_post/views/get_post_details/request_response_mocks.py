


RESPONSE_201_JSON = """
{
    "post_id": 1,
    "posted_by": {
        "name": "string",
        "user_id": 1,
        "profile_pic_url": "string"
    },
    "posted_at": "2099-12-31 00:00:00",
    "post_content": "string",
    "reactions": {
        "count": 1,
        "type": [
            "string"
        ]
    },
    "comments": [
        {
            "comment_id": 1,
            "commenter": {
                "name": "string",
                "user_id": 1,
                "profile_pic_url": "string"
            },
            "commented_at": "2099-12-31 00:00:00",
            "comment_content": "string",
            "reactions": {
                "count": 1,
                "type": [
                    "string"
                ]
            },
            "replies_count": 1,
            "replies": [
                {
                    "comment_id": 1,
                    "commenter": {
                        "name": "string",
                        "user_id": 1,
                        "profile_pic_url": "string"
                    },
                    "commented_at": "2099-12-31 00:00:00",
                    "comment_content": "string",
                    "reactions": {
                        "count": 1,
                        "type": [
                            "string"
                        ]
                    }
                }
            ]
        }
    ],
    "comments_count": 1
}
"""

