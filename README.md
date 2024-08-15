docker build -t gcr.io/translation-api-432204/translation-bot:latest .

docker push gcr.io/translation-api-432204/translation-bot:latest

gcloud run deploy translation-bot-service \
 --image gcr.io/translation-api-432204/translation-bot:latest \
 --platform managed \
 --region us-central1 \
 --allow-unauthenticated
