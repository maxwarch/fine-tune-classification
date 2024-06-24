docker build . -t predict --platform linux/amd64
docker run -p 8001:8001 predict