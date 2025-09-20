pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = '159348431711'
        REPO_NAME = 'visitor-counter-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
        DDB_TABLE = 'VisitorCount'
        EC2_HOST = 'ec2-user@3.90.86.30'
        ECR_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPO_NAME}"
        GIT_BASH_PATH = 'C:\\Program Files\\Git\\bin\\bash.exe'
    }

    stages {

        stage('Checkout') {
            steps {
                retry(3) {
                    checkout scm
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "echo Building Docker image..."
                bat "docker build -t %REPO_NAME%:%IMAGE_TAG% ."
            }
        }

        stage('Login to ECR & Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-creds',
                                                  usernameVariable: 'AWS_ACCESS_KEY_ID',
                                                  passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    bat '''
                        aws configure set aws_access_key_id %AWS_ACCESS_KEY_ID%
                        aws configure set aws_secret_access_key %AWS_SECRET_ACCESS_KEY%
                        aws configure set region %AWS_REGION%

                        for /f "delims=" %%i in ('aws ecr get-login-password --region %AWS_REGION%') do docker login --username AWS --password %%i %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com

                        aws ecr describe-repositories --repository-names %REPO_NAME% || aws ecr create-repository --repository-name %REPO_NAME%

                        docker tag %REPO_NAME%:%IMAGE_TAG% %ECR_URI%:%IMAGE_TAG%
                        docker push %ECR_URI%:%IMAGE_TAG%
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: '89540105-8385-4e62-ad9f-d0e404c254d8',
                                                   keyFileVariable: 'SSH_KEY')]) {
                    bat """
                    "%GIT_BASH_PATH%" -c "ssh -i '$SSH_KEY' -o StrictHostKeyChecking=no %EC2_HOST% \\
                      'aws ecr get-login-password --region %AWS_REGION% | docker login --username AWS --password-stdin %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com && \\
                       docker pull %ECR_URI%:%IMAGE_TAG% && \\
                       docker stop visitorapp || echo Container not running && \\
                       docker rm visitorapp || echo Container not found && \\
                       docker run -d -p 80:5000 --name visitorapp -e AWS_REGION=%AWS_REGION% -e DDB_TABLE=%DDB_TABLE% %ECR_URI%:%IMAGE_TAG%'"
                    """
                }
            }
        }
    }
}

