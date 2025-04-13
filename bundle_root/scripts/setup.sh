#!/usr/bin/env bash
set -e

# common stuff
PACKAGE_NAME=bundle
SLEEP=3

source ../../scripts/common.sh

# create the account to run the build 
gcloud \
    iam service-accounts create ${BUILD_ACCOUNT_NAME} \
    --project=$PROJECT_ID \
    --display-name="${PACKAGE_NAME} build account ${ATTEMPT}" \
    --description="Build account ${ATTEMPT} for ${PACKAGE_NAME}"
sleep $SLEEP

# grants to the account the role to allow write logs to Cloud Logging (used by cloudbuild.yaml)
gcloud \
    projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${BUILD_ACCOUNT_EMAIL}" \
    --role=roles/logging.logWriter \
    --condition=None
sleep $SLEEP

# grants to the account the role to allow write the package into the repo 
gcloud \
    artifacts repositories add-iam-policy-binding $PYTHON_REPO \
    --member="serviceAccount:${BUILD_ACCOUNT_EMAIL}" \
    --role=roles/artifactregistry.writer \
    --condition=None
sleep $SLEEP

# create the trigger, this needs both, the python repository (daisy) and the github 1st gen repository (tekii/daisy)
# to exist.
gcloud \
    builds triggers create github \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --name="bundle-trigger${ATTEMPT_SUFFIX}" \
    --service-account="${BUILD_ACCOUNT}" \
    --repo-owner="tekii" \
    --repo-name="daisy" \
    --branch-pattern="^bundle$" \
    --included-files="bundle_root/**" \
    --ignored-files="bundle_root/scripts/**" \
    --build-config="bundle_root/cloudbuild.yaml" \
    --substitutions="_PYTHON_REPO_URL=${PYTHON_REPO_URL}"
