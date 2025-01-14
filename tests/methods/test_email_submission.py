from datetime import datetime, timezone

import responses

from jmapc import (
    AddedItem,
    Address,
    Client,
    EmailSubmission,
    EmailSubmissionQueryFilterCondition,
    Envelope,
    SetError,
    UndoStatus,
)
from jmapc.methods import (
    EmailSetResponse,
    EmailSubmissionChanges,
    EmailSubmissionChangesResponse,
    EmailSubmissionGet,
    EmailSubmissionGetResponse,
    EmailSubmissionQuery,
    EmailSubmissionQueryChanges,
    EmailSubmissionQueryChangesResponse,
    EmailSubmissionQueryResponse,
    EmailSubmissionSet,
    EmailSubmissionSetResponse,
)

from ..utils import expect_jmap_call

expected_request_create = {
    "emailToSend": {
        "emailId": "#draft",
        "identityId": "1000",
        "envelope": {
            "mailFrom": {
                "email": "ness@onett.example.com",
                "parameters": None,
            },
            "rcptTo": [
                {
                    "email": "ness@onett.example.com",
                    "parameters": None,
                }
            ],
        },
    }
}
email_submission_set_response = {
    "accountId": "u1138",
    "created": {
        "emailToSend": {
            "id": "S2000",
            "sendAt": "1994-08-24T12:01:02Z",
            "undoStatus": "final",
        }
    },
    "updated": None,
    "destroyed": None,
    "oldState": "1",
    "newState": "2",
    "notCreated": None,
    "notUpdated": None,
    "notDestroyed": None,
}


def test_email_submission_changes(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "EmailSubmission/changes",
                {
                    "accountId": "u1138",
                    "sinceState": "2999",
                    "maxChanges": 47,
                },
                "single.EmailSubmission/changes",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "EmailSubmission/changes",
                {
                    "accountId": "u1138",
                    "oldState": "2999",
                    "newState": "3000",
                    "hasMoreChanges": False,
                    "created": ["S0001", "S0002"],
                    "updated": [],
                    "destroyed": ["S0003"],
                },
                "single.EmailSubmission/changes",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        EmailSubmissionChanges(since_state="2999", max_changes=47)
    ) == EmailSubmissionChangesResponse(
        account_id="u1138",
        old_state="2999",
        new_state="3000",
        has_more_changes=False,
        created=["S0001", "S0002"],
        updated=[],
        destroyed=["S0003"],
    )


def test_email_submission_get(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "EmailSubmission/get",
                {
                    "accountId": "u1138",
                    "ids": ["S2000"],
                },
                "single.EmailSubmission/get",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "EmailSubmission/get",
                {
                    "accountId": "u1138",
                    "state": "2187",
                    "notFound": [],
                    "list": [
                        {
                            "id": "S2000",
                            "undoStatus": "final",
                            "sendAt": "1994-08-24T12:01:02Z",
                        }
                    ],
                },
                "single.EmailSubmission/get",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        EmailSubmissionGet(ids=["S2000"])
    ) == EmailSubmissionGetResponse(
        account_id="u1138",
        state="2187",
        not_found=[],
        data=[
            EmailSubmission(
                id="S2000",
                undo_status=UndoStatus.FINAL,
                send_at=datetime(1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc),
            ),
        ],
    )


def test_email_submission_query(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "EmailSubmission/query",
                {
                    "accountId": "u1138",
                    "filter": {
                        "undoStatus": "final",
                    },
                },
                "single.EmailSubmission/query",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "EmailSubmission/query",
                {
                    "accountId": "u1138",
                    "ids": ["S2000", "S2001"],
                    "queryState": "4000",
                    "canCalculateChanges": True,
                    "position": 42,
                    "total": 9001,
                    "limit": 256,
                },
                "single.EmailSubmission/query",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        EmailSubmissionQuery(
            filter=EmailSubmissionQueryFilterCondition(
                undo_status=UndoStatus.FINAL,
            )
        )
    ) == EmailSubmissionQueryResponse(
        account_id="u1138",
        ids=["S2000", "S2001"],
        query_state="4000",
        can_calculate_changes=True,
        position=42,
        total=9001,
        limit=256,
    )


def test_email_submission_query_changes(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "EmailSubmission/queryChanges",
                {
                    "accountId": "u1138",
                    "filter": {
                        "undoStatus": "final",
                    },
                    "sinceQueryState": "1000",
                    "calculateTotal": False,
                },
                "single.EmailSubmission/queryChanges",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "EmailSubmission/queryChanges",
                {
                    "accountId": "u1138",
                    "oldQueryState": "1000",
                    "newQueryState": "1003",
                    "added": [
                        {
                            "id": "S2000",
                            "index": 3,
                        },
                        {
                            "id": "S2001",
                            "index": 8,
                        },
                    ],
                    "removed": ["S2008"],
                    "total": 42,
                },
                "single.EmailSubmission/queryChanges",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        EmailSubmissionQueryChanges(
            filter=EmailSubmissionQueryFilterCondition(
                undo_status=UndoStatus.FINAL
            ),
            since_query_state="1000",
        )
    ) == EmailSubmissionQueryChangesResponse(
        account_id="u1138",
        old_query_state="1000",
        new_query_state="1003",
        removed=["S2008"],
        added=[
            AddedItem(id="S2000", index=3),
            AddedItem(id="S2001", index=8),
        ],
        total=42,
    )


def test_email_submission_set(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "EmailSubmission/set",
                {
                    "accountId": "u1138",
                    "create": expected_request_create,
                },
                "single.EmailSubmission/set",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "EmailSubmission/set",
                email_submission_set_response,
                "single.EmailSubmission/set",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        EmailSubmissionSet(
            create=dict(
                emailToSend=EmailSubmission(
                    email_id="#draft",
                    identity_id="1000",
                    envelope=Envelope(
                        mail_from=Address(email="ness@onett.example.com"),
                        rcpt_to=[Address(email="ness@onett.example.com")],
                    ),
                )
            )
        )
    ) == EmailSubmissionSetResponse(
        account_id="u1138",
        old_state="1",
        new_state="2",
        created=dict(
            emailToSend=EmailSubmission(
                id="S2000",
                undo_status=UndoStatus.FINAL,
                send_at=datetime(1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc),
            ),
        ),
        updated=None,
        destroyed=None,
        not_created=None,
        not_updated=None,
        not_destroyed=None,
    )


def test_email_submission_set_on_success_destroy_email(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "EmailSubmission/set",
                {
                    "accountId": "u1138",
                    "create": expected_request_create,
                    "onSuccessDestroyEmail": ["#emailToSend"],
                },
                "single.EmailSubmission/set",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "EmailSubmission/set",
                email_submission_set_response,
                "single.EmailSubmission/set",
            ],
            [
                "Email/set",
                {
                    "accountId": "u1138",
                    "oldState": "2",
                    "newState": "3",
                    "created": None,
                    "updated": None,
                    "destroyed": ["Mdeadbeefdeadbeefdeadbeef"],
                    "notCreated": None,
                    "notUpdated": None,
                    "notDestroyed": None,
                },
                "single.EmailSubmission/set",
            ],
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        EmailSubmissionSet(
            on_success_destroy_email=["#emailToSend"],
            create=dict(
                emailToSend=EmailSubmission(
                    email_id="#draft",
                    identity_id="1000",
                    envelope=Envelope(
                        mail_from=Address(email="ness@onett.example.com"),
                        rcpt_to=[Address(email="ness@onett.example.com")],
                    ),
                )
            ),
        )
    ) == [
        EmailSubmissionSetResponse(
            account_id="u1138",
            old_state="1",
            new_state="2",
            created=dict(
                emailToSend=EmailSubmission(
                    id="S2000",
                    undo_status=UndoStatus.FINAL,
                    send_at=datetime(
                        1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc
                    ),
                ),
            ),
            updated=None,
            destroyed=None,
            not_created=None,
            not_updated=None,
            not_destroyed=None,
        ),
        EmailSetResponse(
            account_id="u1138",
            old_state="2",
            new_state="3",
            created=None,
            updated=None,
            destroyed=["Mdeadbeefdeadbeefdeadbeef"],
            not_created=None,
            not_updated=None,
            not_destroyed=None,
        ),
    ]


def test_email_submission_set_on_success_update_email(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "EmailSubmission/set",
                {
                    "accountId": "u1138",
                    "create": expected_request_create,
                    "onSuccessUpdateEmail": {
                        "keywords/$draft": None,
                    },
                },
                "single.EmailSubmission/set",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "EmailSubmission/set",
                email_submission_set_response,
                "single.EmailSubmission/set",
            ],
            [
                "Email/set",
                {
                    "accountId": "u1138",
                    "oldState": "2",
                    "newState": "3",
                    "created": None,
                    "updated": {
                        "Mdeadbeefdeadbeefdeadbeef": None,
                    },
                    "destroyed": None,
                    "notCreated": None,
                    "notUpdated": None,
                    "notDestroyed": None,
                },
                "single.EmailSubmission/set",
            ],
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        EmailSubmissionSet(
            on_success_update_email={
                "keywords/$draft": None,
            },
            create=dict(
                emailToSend=EmailSubmission(
                    email_id="#draft",
                    identity_id="1000",
                    envelope=Envelope(
                        mail_from=Address(email="ness@onett.example.com"),
                        rcpt_to=[Address(email="ness@onett.example.com")],
                    ),
                )
            ),
        )
    ) == [
        EmailSubmissionSetResponse(
            account_id="u1138",
            old_state="1",
            new_state="2",
            created=dict(
                emailToSend=EmailSubmission(
                    id="S2000",
                    undo_status=UndoStatus.FINAL,
                    send_at=datetime(
                        1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc
                    ),
                ),
            ),
            updated=None,
            destroyed=None,
            not_created=None,
            not_updated=None,
            not_destroyed=None,
        ),
        EmailSetResponse(
            account_id="u1138",
            old_state="2",
            new_state="3",
            created=None,
            updated={"Mdeadbeefdeadbeefdeadbeef": None},
            destroyed=None,
            not_created=None,
            not_updated=None,
            not_destroyed=None,
        ),
    ]


def test_email_submission_set_update_email_error(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "EmailSubmission/set",
                {
                    "accountId": "u1138",
                    "create": expected_request_create,
                    "onSuccessUpdateEmail": {
                        "keywords/$draft": None,
                        "mailboxIds/MBX5": None,
                    },
                },
                "single.EmailSubmission/set",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "EmailSubmission/set",
                email_submission_set_response,
                "single.EmailSubmission/set",
            ],
            [
                "Email/set",
                {
                    "accountId": "u1138",
                    "oldState": "2",
                    "newState": "3",
                    "created": None,
                    "updated": None,
                    "destroyed": None,
                    "notCreated": None,
                    "notUpdated": {
                        "Mdeadbeefdeadbeefdeadbeef": {
                            "type": "invalidProperties",
                            "properties": ["mailboxIds"],
                        },
                    },
                    "notDestroyed": None,
                },
                "single.EmailSubmission/set",
            ],
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        EmailSubmissionSet(
            on_success_update_email={
                "keywords/$draft": None,
                "mailboxIds/MBX5": None,
            },
            create=dict(
                emailToSend=EmailSubmission(
                    email_id="#draft",
                    identity_id="1000",
                    envelope=Envelope(
                        mail_from=Address(email="ness@onett.example.com"),
                        rcpt_to=[Address(email="ness@onett.example.com")],
                    ),
                )
            ),
        )
    ) == [
        EmailSubmissionSetResponse(
            account_id="u1138",
            old_state="1",
            new_state="2",
            created=dict(
                emailToSend=EmailSubmission(
                    id="S2000",
                    undo_status=UndoStatus.FINAL,
                    send_at=datetime(
                        1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc
                    ),
                ),
            ),
            updated=None,
            destroyed=None,
            not_created=None,
            not_updated=None,
            not_destroyed=None,
        ),
        EmailSetResponse(
            account_id="u1138",
            old_state="2",
            new_state="3",
            created=None,
            updated=None,
            destroyed=None,
            not_created=None,
            not_updated={
                "Mdeadbeefdeadbeefdeadbeef": SetError(
                    type="invalidProperties", description=None
                )
            },
            not_destroyed=None,
        ),
    ]
