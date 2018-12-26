
sam validate sam-app\template.yaml

sam package  --template-file sam-app\template.yaml    --output-template-file serverless-output.yaml   --s3-bucket my-rudolph-package 

aws cloudformation deploy --template-file C:\Users\rickerg\git\rudolph\serverless-output.yaml --stack-name rudolph --capabilities CAPABILITY_IAM

aws cloudformation describe-stack-events --stack-name rudolph


pip install pip-tools

pip-compile --output-file requirements-dev.txt  requirements.txt