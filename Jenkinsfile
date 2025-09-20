pipeline {
  agent any

  environment {
    AWS_REGION = 'us-east-1'
    AWS_ACCOUNT_ID = '159348431711'    // set in Jenkins job or replace here
    REPO_NAME = 'visitor-counter-app'
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    DDB_TABLE = 'VisitorCount'
    EC2_HOST = 'ec2-user@3.90.86.30'
    ECR_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPO_NAME}"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build image') {
      steps {
        sh "docker build -t ${REPO_NAME}:${IMAGE_TAG} ."
      }
    }

    stage('Login to ECR & Push') {
      steps {
        // Bind AWS keys stored in Jenkins as username/password (username=ACCESS_KEY, password=SECRET)
        withCredentials([usernamePassword(credentialsId: 'aws-creds',
                                          usernameVariable: 'AWS_ACCESS_KEY_ID',
                                          passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
          sh '''
            aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
            aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
            aws configure set region $AWS_REGION

            aws ecr get-login-password --region $AWS_REGION | \
              docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

            # ensure repo exists
            aws ecr describe-repositories --repository-names ${REPO_NAME} || \
              aws ecr create-repository --repository-name ${REPO_NAME}

            docker tag ${REPO_NAME}:${IMAGE_TAG} ${ECR_URI}:${IMAGE_TAG}
            docker push ${ECR_URI}:${IMAGE_TAG}
          '''
        }
      }
    }

    stage('Deploy to EC2') {
      steps {
        sshagent(['ec2-ssh-key']) {
          sh """
            ssh -o StrictHostKeyChecking=no ${EC2_HOST} \\
              "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com && \
               docker pull ${ECR_URI}:${IMAGE_TAG} && \
               docker stop visitorapp || true && docker rm visitorapp || true && \
               docker run -d -p 80:5000 --name visitorapp -e AWS_REGION=${AWS_REGION} -e DDB_TABLE=${DDB_TABLE} ${ECR_URI}:${IMAGE_TAG}"
          """
        }
      }
    }
  }
}
