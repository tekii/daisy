#!/usr/bin/env bash
set -e

# common stuff
PACKAGE_NAME=ingestor
SLEEP=5

source ../../scripts/common.sh

INGESTOR_ACCOUNT_EMAIL="ingestor@${PROJECT_ID}.iam.gserviceaccount.com"

#
# TEST ACCOUNT
#
TEST_ACCOUNT_NAME=${PACKAGE_NAME}-test${ATTEMPT_SUFFIX}
TEST_ACCOUNT_EMAIL="${TEST_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
TEST_ACCOUNT="projects/${PROJECT_ID}/serviceAccounts/${TEST_ACCOUNT_EMAIL}"

gcloud \
    iam service-accounts create ${TEST_ACCOUNT_NAME} \
    --project=$PROJECT_ID \
    --display-name="${PACKAGE_NAME} test account ${ATTEMPT}" \
    --description="Test account ${ATTEMPT} for service ${PACKAGE_NAME} "
sleep $SLEEP

gcloud \
    projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${TEST_ACCOUNT_EMAIL}" \
    --role=roles/logging.logWriter \
    --condition=None
sleep $SLEEP

gcloud iam service-accounts add-iam-policy-binding "${INGESTOR_ACCOUNT_EMAIL}" \
    --project=$PROJECT_ID \
    --member="serviceAccount:${TEST_ACCOUNT_EMAIL}" \
    --role=roles/iam.serviceAccountTokenCreator \
    --condition=None
sleep $SLEEP