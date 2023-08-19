aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 235713525425.dkr.ecr.ap-northeast-2.amazonaws.com

docker build --platform linux/amd64  -t juncsync-be .
docker tag juncsync-be 235713525425.dkr.ecr.ap-northeast-2.amazonaws.com/juncsync-be

docker push 235713525425.dkr.ecr.ap-northeast-2.amazonaws.com/juncsync-be