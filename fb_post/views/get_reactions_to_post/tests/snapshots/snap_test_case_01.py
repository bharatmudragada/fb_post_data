# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01GetReactionsToPostAPITestCase::test_case status'] = 201

snapshots['TestCase01GetReactionsToPostAPITestCase::test_case body'] = [
    {
        'name': 'username',
        'profile_pic': '',
        'reaction': 'LOVE',
        'user_id': 1
    }
]

snapshots['TestCase01GetReactionsToPostAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '75',
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
