#!/usr/bin/env bash

# common stuff
MODULE=toolbox
ACCOUNT_NUMBER=19

source ../../scripts/common.sh

SERVICE_ACCOUNT_NAME=${MODULE}-${PROJECT_NUMBER}-${ACCOUNT_NUMBER}

if [ ${#SERVICE_ACCOUNT_NAME} -ge 30 ]; then echo "SERVICE_ACCOUNT_NAME too long"; exit 1 
else echo $SERVICE_ACCOUNT_NAME ${#SERVICE_ACCOUNT_NAME}
fi

SERVICE_ACCOUNT="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo $PROJECT_ID
echo $PROJECT_NUMBER
echo $LOCATION
echo $SERVICE_ACCOUNT

# create the builder
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
    --project=$PROJECT_ID \
    --display-name="BT ${MODULE}" \
    --description="Builder / tester for ${MODULE}"
sleep 10

# gcloud <resourceType> add-iam-policy-binding <resourceName> 
# --member=<accountToGrantOnTheResource> --role=<roleToGrantOnTheResource>

# grants the role to allow write logs to Cloud Logging (used by cloudbuild.yaml)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role=roles/logging.logWriter \
    --condition=None
sleep 10

# grants the role to allow write the package into the repo 
# https://cloud.google.com/artifact-registry/docs/access-control#roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role=roles/artifactregistry.writer \
    --condition=None
