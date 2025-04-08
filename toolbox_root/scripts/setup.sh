#!/usr/bin/env bash
set -e

# common stuff
MODULE_NAME=toolbox
ATTEMPT_SUFFIX="-24"
SLEEP=3

source ../../scripts/common.sh

# create the account to run the build 
gcloud \
    iam service-accounts create ${DEPLOY_ACCOUNT_NAME} \
    --project=$PROJECT_ID \
    --display-name="Builder ${ATTEMPT_SUFFIX} ${MODULE_NAME}" \
    --description="Builder / tester ${ATTEMPT_SUFFIX} for ${MODULE_NAME} "
sleep $SLEEP

# grants to the account the role to allow write logs to Cloud Logging (used by cloudbuild.yaml)
gcloud \
    projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${DEPLOY_ACCOUNT}" \
    --role=roles/logging.logWriter \
    --condition=None
sleep $SLEEP

# grants to the account the role to allow write the package into the repo 
gcloud \
    artifacts repositories add-iam-policy-binding $PYTHON_REPO_FULL_NAME \
    --member="serviceAccount:${DEPLOY_ACCOUNT}" \
    --role=roles/artifactregistry.writer \
    --condition=None
sleep $SLEEP

# create the trigger, this needs both, the python repository (daisy) and the github 1st gen repository (tekii/daisy)
# to exist.
gcloud \
    builds triggers create github \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --name="toolbox-packages${ATTEMPT_SUFFIX}" \
    --service-account="projects/${PROJECT_ID}/serviceAccounts/${DEPLOY_ACCOUNT}" \
    --repo-owner="tekii" \
    --repo-name="daisy" \
    --branch-pattern="^toolbox$" \
    --included-files="toolbox_root/**" \
    --build-config="toolbox_root/cloudbuild.yaml" \
    --substitutions="_PYTHON_REPO_URL=${PYTHON_REPO_URL}"
#   --substitutions="_ARTIFACT_REPO=${PYTHON_REPO_FULL_NAME}"
