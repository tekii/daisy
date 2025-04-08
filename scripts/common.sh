# project
PROJECT_ID="${1:-daisy-tekii}"
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
LOCATION="us-central1"
# attempt prompt
read -r -p "Enter attempt number [0-99]: " attempt
if ! ((  0 <= "$attempt" && "$attempt" <= 99 )); then echo "Invalid ATTEMPT_SUFFIX: ${attempt}"; exit 1 
fi
ATTEMPT_SUFFIX="-${attempt}"
# account
DEPLOY_ACCOUNT_NAME=${MODULE_NAME}-${PROJECT_NUMBER}${ATTEMPT_SUFFIX}
if [ ${#DEPLOY_ACCOUNT_NAME} -ge 30 ]; then echo "DEPLOY_ACCOUNT_NAME too long"; exit 1 
else echo $DEPLOY_ACCOUNT_NAME ${#DEPLOY_ACCOUNT_NAME}
fi
DEPLOY_ACCOUNT="${DEPLOY_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
# repos
PYTHON_REPO_NAME="margot"
PYTHON_REPO_FULL_NAME="projects/${PROJECT_ID}/locations/${LOCATION}/repositories/${PYTHON_REPO_NAME}"
PYTHON_REPO_URL=$(gcloud artifacts repositories describe $PYTHON_REPO_FULL_NAME --format="value(registryUri)")
DOCKER_REPO_FULL_NAME="projects/${PROJECT_ID}/locations/${LOCATION}/repositories/images"
DOCKER_REPO_URL=$(gcloud artifacts repositories describe $DOCKER_REPO_FULL_NAME --format="value(registryUri)")

echo $PROJECT_ID
echo $PROJECT_NUMBER
echo $LOCATION
echo $DEPLOY_ACCOUNT
echo $PYTHON_REPO_FULL_NAME
echo $PYTHON_REPO_URL
echo $DOCKER_REPO_FULL_NAME
echo $DOCKER_REPO_URL

# 
read -r -p "Are you sure? [y/N] " response
case "$response" in 
    [yY][eE][sS]|[yY]) 
        ;;
    *)
        echo "Bye..."
        exit 1
        ;;
esac
