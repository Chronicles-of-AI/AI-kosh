docker run -d \
    -p 8000:8000 \
    -v "$(pwd)":/app \
    --name text_classification text_classification