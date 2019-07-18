# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01GetRepliesToCommentAPITestCase::test_case status'] = 201

snapshots['TestCase01GetRepliesToCommentAPITestCase::test_case body'] = [
    {
        'comment_content': 'This is a reply',
        'comment_id': 2,
        'commented_at': '19-08-18 00:00:00.000000',
        'commenter': {
            'name': 'username',
            'profile_pic_url': '',
            'user_id': 1
        }
    },
    {
        'comment_content': 'This is a 2 reply',
        'comment_id': 3,
        'commented_at': '19-08-18 00:00:00.000000',
        'commenter': {
            'name': 'username',
            'profile_pic_url': '',
            'user_id': 1
        }
    }
]

snapshots['TestCase01GetRepliesToCommentAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '348',
        'Content-Length'
    ],
    'content-type': [
        'Content-Type',
        'text/html; charset=utf-8'
    ],
    'vary': [
        'Accept-Language, Origin, Cookie',
        'Vary'
    ],
    'x-frame-options': [
        'SAMEORIGIN',
        'X-Frame-Options'
    ]
}
