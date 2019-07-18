# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01GetUserPostsAPITestCase::test_case status'] = 201

snapshots['TestCase01GetUserPostsAPITestCase::test_case body'] = [
    {
        'comments': [
        ],
        'comments_count': 0,
        'post_content': 'This is first post',
        'post_id': 1,
        'posted_at': '19-07-18 15:44:12.069897',
        'posted_by': {
            'name': 'user1',
            'profile_pic_url': '',
            'user_id': 1
        },
        'reactions': {
            'count': 0,
            'type': [
            ]
        }
    },
    {
        'comments': [
        ],
        'comments_count': 0,
        'post_content': 'This is second post',
        'post_id': 2,
        'posted_at': '19-07-18 15:44:12.070105',
        'posted_by': {
            'name': 'user1',
            'profile_pic_url': '',
            'user_id': 1
        },
        'reactions': {
            'count': 0,
            'type': [
            ]
        }
    },
    {
        'comments': [
        ],
        'comments_count': 0,
        'post_content': 'This is third post',
        'post_id': 3,
        'posted_at': '19-07-18 15:44:12.070257',
        'posted_by': {
            'name': 'user1',
            'profile_pic_url': '',
            'user_id': 1
        },
        'reactions': {
            'count': 0,
            'type': [
            ]
        }
    }
]

snapshots['TestCase01GetUserPostsAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '721',
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
