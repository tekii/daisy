#!/usr/bin/env python3

import sys
import configparser

import google.auth
from google.oauth2 import service_account
from google.auth.exceptions import GoogleAuthError

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# import httplib2

import time


def main(argv):
    # TODO handle IO errors
    #
    # parser = configparser.ConfigParser()
    # parser.read_file(open(".attic/config"))
    topic = "projects/daisy-dev01/topics/gmail-watch"  # parser.get("configs", "TOPIC")
    label = "INBOX"  # parser.get("configs", "LABEL")
    scopes = "https://www.googleapis.com/auth/gmail.readonly"
    try:

        credentials, project = google.auth.default()
        project = None
        if not project:
            credentials = service_account.Credentials.from_service_account_file(
                #'daisy-dev01-01822f99f16b.json',
                "../.secrets/mock_credentials.json",
                scopes=[scopes],
                subject="queue@margot.tekii.com.ar",  # argv[1],
            )

        # credentials = ServiceAccountCredentials.retrieve_scopes()
        # http = httplib2.Http()
        # http = delegated.authorize(http)
        # response, content = http.request("https://www.google.com")

        # cred, project = google.auth.default(scopes=scopes)

        delegated = credentials  # .with_subject(argv[1])

        service = build("gmail", "v1", credentials=delegated)

        request = {"labelIds": [label], "topicName": topic}

        # Call the Gmail API to watch given mailbox label ('me indicated the authenticated user')
        result = service.users().watch(userId="me", body=request).execute()
        print(result)

        result = service.users().getProfile(userId="me").execute()
        print(result)
        # https://developers.google.com/gmail/api/reference/rest/v1/users/watch#response-body

        time.sleep(5)

        result = service.users().stop(userId="me").execute()
        print(result)

    except GoogleAuthError as e:
        print("An error occurred GoogleAuth: %s" % e)
    #    except HttpAccessTokenRefreshError as e:
    #        print('An error occurred HttpAccessTokenRefreshError: %s' % e)
    # todo sub errors
    except HttpError as err:
        print("An error occurred HttpError: %s" % err)


if __name__ == "__main__":
    main(sys.argv)
