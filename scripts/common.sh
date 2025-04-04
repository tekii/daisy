#
PROJECT_ID="${1:-daisy-tekii}"
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
LOCATION="us-central1"
