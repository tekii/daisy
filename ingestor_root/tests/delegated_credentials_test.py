from googleapiclient.discovery import build  # type: ignore[import-untyped]

from mail.delegated_credentials import get_subject_credentials_from_impersonated


def test_get_dwd_credentials():

    credentials = get_subject_credentials_from_impersonated(
        subject_email="queue@margot.tekii.com.ar",
        subject_scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        lifetime=360,
    )

    topic = "projects/daisy-dev01/topics/gmail-watch"
    label = "INBOX"

    client = build("gmail", "v1", credentials=credentials)
    request = {"labelIds": [label], "topicName": topic}
    # Call the Gmail API to watch given mailbox label ('me indicated the authenticated user')
    _ = client.users().watch(userId="me", body=request).execute()
    client.users().stop(userId="me").execute()
    pass
