
#call aws s3api delete-bucket --bucket my-reindeer-dropzone --region us-east-1
call aws s3api create-bucket --bucket my-rudolph-package --region us-east-1

#call aws cloudformation delete-stack --stack-name  rudolph

echo delete zip file.
del backgroundpackage.zip
del ondemandpackage.zip

7z  a -tzip backgroundpackage.zip  .\rudolph\backgroundfunction\backgroundfunction.py  
7z  a -tzip ondemandpackage.zip  .\rudolph\OnDemand\ondemandfunction.py  


echo copy.
call aws s3 cp backgroundpackage.zip s3://my-rudolph-package/backgroundpackage.zip
call aws s3 cp ondemandpackage.zip s3://my-rudolph-package/ondemandpackage.zip


echo package.
call sam package  --template-file template.yaml    --output-template-file serverless-output.yaml   --s3-bucket my-rudolph-package


echo deploy.
call aws cloudformation deploy --template-file C:\Users\rickerg\git\rudolph\sam-app\serverless-output.yaml --stack-name rudolph --capabilities CAPABILITY_IAM

