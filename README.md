# rpg-char-generator
Web application that generates a character with predefined stats based on the class you choose.

## Build
The buildspec.yaml file contains the collection of build commands to be run in AWS CodeBuild. The build installs kubectl, builds the docker image from the latest source code changes and pushes it to ECR. After the image is uploaded, a rolling update is initiated to a deployment in a kubernetes cluster.

For this to work, you need to authenticate the CodeBuild Service role will the k8s cluster. This is done by adding an entry to the aws-auth config map with the appropriate RBAC permissions.
