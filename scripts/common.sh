# project
PROJECT_ID="${1:-daisy-tekii}"
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
LOCATION="us-central1"
ATTEMPT_SUFFIX=$(<ATTEMPT)
# account
SERVICE_ACCOUNT_NAME=${MODULE_NAME}-${PROJECT_NUMBER}${ATTEMPT_SUFFIX}
if [ ${#SERVICE_ACCOUNT_NAME} -ge 30 ]; then echo "SERVICE_ACCOUNT_NAME too long"; exit 1 
else echo $SERVICE_ACCOUNT_NAME ${#SERVICE_ACCOUNT_NAME}
fi
SERVICE_ACCOUNT="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
# repos
PYTHON_REPO_NAME="margot"
PYTHON_REPO_FULL_NAME="projects/${PROJECT_ID}/locations/${LOCATION}/repositories/${PYTHON_REPO_NAME}"
PYTHON_REPO_URL=$(gcloud artifacts repositories describe $PYTHON_REPO_FULL_NAME --format="value(registryUri)")
DOCKER_REPO_FULL_NAME="projects/${PROJECT_ID}/locations/${LOCATION}/repositories/images"
DOCKER_REPO_URL=$(gcloud artifacts repositories describe $DOCKER_REPO_FULL_NAME --format="value(registryUri)")

echo $PROJECT_ID
echo $PROJECT_NUMBER
echo $LOCATION
echo $SERVICE_ACCOUNT
echo $PYTHON_REPO_FULL_NAME
echo $PYTHON_REPO_URL
echo $DOCKER_REPO_FULL_NAME
echo $DOCKER_REPO_URL
