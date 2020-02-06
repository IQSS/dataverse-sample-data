void setBuildStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "${env.GIT_URL}"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/docker/dataverse-sample-data"],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}

pipeline {
  agent any
  environment {
    DOCKER_IMAGE_NAME = "iqss/dataverse-sample-data"
    DOCKER_IMAGE_TAG = "build-${env.BRANCH_NAME}"
    DOCKER_WORKDIR = "."
    DOCKER_HUB_CRED = "dockerhub-dataversebot"
    DOCKER_REGISTRY = "https://registry.hub.docker.com"
  }
  stages {
    stage('build') {
      when {
        anyOf {
          branch 'master'
          branch 'PR-14'
        }
      }
      steps {
        script {
          docker_image = docker.build("${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG}", "--pull ${env.DOCKER_WORKDIR}")
        }
      }
    }
    stage('push') {
      when {
        anyOf {
          branch 'master'
          branch 'PR-14'
        }
      }
      steps {
        script {
          // Push master image to latest tag
          docker.withRegistry("${env.DOCKER_REGISTRY}", "${env.DOCKER_HUB_CRED}") {
            docker_image.push("latest")
          }
        }
      }
    }
  }
  post {
    success {
        setBuildStatus("Image build and push succeeded", "SUCCESS");
    }
    failure {
        setBuildStatus("Image build or push failed", "FAILURE");
    }
  }
}
