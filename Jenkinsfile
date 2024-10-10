pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Padliwinata/faker-pipelilne.git'
            }
        }

        stage('Build and Deploy with Docker Compose') {
            steps {
                script {
                    // Ensure previous containers are stopped
                    sh 'docker-compose down'

                    // Build and bring up the services defined in docker-compose.yml
                    sh 'docker-compose up --build -d'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline execution failed.'
        }
    }
}
