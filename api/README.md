run : uv run main.py
uv run --with jupyter jupyter lab

docker build -t ai .
docker build --platform linux/arm64 -f dockerfile-lambda -t ai-lambda .
docker tag ai-lambda 376940595896.dkr.ecr.ap-northeast-2.amazonaws.com/fingoo-ai
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 376940595896.dkr.ecr.ap-northeast-2.amazonaws.com
docker push 376940595896.dkr.ecr.ap-northeast-2.amazonaws.com/fingoo-ai
