docker run -d \
    -p 5000:5000 \
    -v "$(pwd)":/app \
    --name image_classification image_classification