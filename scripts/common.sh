# project
PROJECT_ID="${1:-daisy-tekii}"
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
LOCATION="us-central1"
# ATTEMPT prompt
read -r -p "Enter ATTEMPT number [0-99]: " ATTEMPT
if ! ((  0 <= "$ATTEMPT" && "$ATTEMPT" <= 99 )); then echo "Invalid ATTEMPT_SUFFIX: ${ATTEMPT}"; exit 1 
fi
ATTEMPT_SUFFIX="-${ATTEMPT}"
# account
BUILD_ACCOUNT_NAME=${PACKAGE_NAME}-deploy${ATTEMPT_SUFFIX}
if [ ${#BUILD_ACCOUNT_NAME} -ge 30 ]; then echo "BUILD_ACCOUNT_NAME too long"; exit 1 
else echo $BUILD_ACCOUNT_NAME ${#BUILD_ACCOUNT_NAME}
fi
BUILD_ACCOUNT_EMAIL="${BUILD_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
BUILD_ACCOUNT="projects/${PROJECT_ID}/serviceAccounts/${BUILD_ACCOUNT_EMAIL}"
# repos
PYTHON_REPO_NAME="margot"
PYTHON_REPO="projects/${PROJECT_ID}/locations/${LOCATION}/repositories/${PYTHON_REPO_NAME}"
PYTHON_REPO_URL=$(gcloud artifacts repositories describe $PYTHON_REPO --format="value(registryUri)")
DOCKER_REPO="projects/${PROJECT_ID}/locations/${LOCATION}/repositories/images"
DOCKER_REPO_URL=$(gcloud artifacts repositories describe $DOCKER_REPO --format="value(registryUri)")

echo $PROJECT_ID
echo $PROJECT_NUMBER
echo $LOCATION
echo $BUILD_ACCOUNT_EMAIL
echo $BUILD_ACCOUNT
echo $PYTHON_REPO
echo $PYTHON_REPO_URL
echo $DOCKER_REPO
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
