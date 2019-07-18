# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase02AddReplyToCommentAPITestCase::test_case status'] = 201

snapshots['TestCase02AddReplyToCommentAPITestCase::test_case body'] = {
    'reply_comment_id': 3
}

snapshots['TestCase02AddReplyToCommentAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '23',
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

snapshots['TestCase02AddReplyToCommentAPITestCase::test_case post_id'] = 1

snapshots['TestCase02AddReplyToCommentAPITestCase::test_case commented_on_id'] = 1

snapshots['TestCase02AddReplyToCommentAPITestCase::test_case user_id'] = 1

snapshots['TestCase02AddReplyToCommentAPITestCase::test_case comment_text'] = 'This is reply to reply'
