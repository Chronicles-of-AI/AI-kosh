docker run -d \
    -p 8080:8080 \
    -v "$(pwd)":/app \
    --name image_classification image_classification