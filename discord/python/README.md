This is a tempalte for dicord interaction endpoint executed via aws lambda functions, 

# prerequisites
- need dependecies for nacl install using `pip install pynacl`
- package the deps with lambda handler into zip 
    - refer to [Lambda docs](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-dependencies)
-  need discord bot public key as env var DISCORD_PUBLIC_KEY
