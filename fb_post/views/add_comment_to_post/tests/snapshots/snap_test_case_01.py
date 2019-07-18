# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01AddCommentToPostAPITestCase::test_case status'] = 201

snapshots['TestCase01AddCommentToPostAPITestCase::test_case body'] = {
    'comment_id': 1
}

snapshots['TestCase01AddCommentToPostAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '17',
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

snapshots['TestCase01AddCommentToPostAPITestCase::test_case comment_text'] = 'This is comment to post'

snapshots['TestCase01AddCommentToPostAPITestCase::test_case count_difference'] = 1

snapshots['TestCase01AddCommentToPostAPITestCase::test_case user_id'] = 1

snapshots['TestCase01AddCommentToPostAPITestCase::test_case post_id'] = 1
