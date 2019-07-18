# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01GetReactionMetricsAPITestCase::test_case status'] = 201

snapshots['TestCase01GetReactionMetricsAPITestCase::test_case body'] = [
    {
        'count': 2,
        'reaction_type': 'LIKE'
    },
    {
        'count': 1,
        'reaction_type': 'LOVE'
    },
    {
        'count': 1,
        'reaction_type': 'SAD'
    }
]

snapshots['TestCase01GetReactionMetricsAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '116',
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
