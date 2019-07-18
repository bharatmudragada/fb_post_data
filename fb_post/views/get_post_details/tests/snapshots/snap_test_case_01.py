# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01GetPostDetailsAPITestCase::test_case status'] = 201

snapshots['TestCase01GetPostDetailsAPITestCase::test_case body'] = {
    'comments': [
        {
            'comment_content': 'This is comment',
            'comment_id': 1,
            'commented_at': '19-08-18 00:00:00.000000',
            'commenter': {
                'name': 'user1',
                'profile_pic_url': '',
                'user_id': 1
            },
            'reactions': {
                'count': 3,
                'type': [
                    'LOVE',
                    'WOW'
                ]
            },
            'replies': [
                {
                    'comment_content': 'This is reply',
                    'comment_id': 2,
                    'commented_at': '19-08-18 00:00:00.000000',
                    'commenter': {
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
            ],
            'replies_count': 1
        }
    ],
    'comments_count': 1,
    'post_content': 'This is first post',
    'post_id': 1,
    'posted_at': '19-08-18 00:00:00.000000',
    'posted_by': {
        'name': 'user1',
        'profile_pic_url': '',
        'user_id': 1
    },
    'reactions': {
        'count': 2,
        'type': [
            'WOW'
        ]
    }
}

snapshots['TestCase01GetPostDetailsAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '703',
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
