pipeline {
  agent any
  stages {
    stage('Pull') {
      steps {
        git 'https://github.com/build1244/python.git'
      }
    }

    stage('docker-compose') {
      steps {
        sh 'docker-compose up --build -d'
      }
    }

  }
}