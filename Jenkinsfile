pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Cloner le dépôt GitHub
                git branch: 'main', url: 'https://github.com/hossain109/webscrapping-automation.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Create and activate a virtual environment
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && python3 -m pip install -r requirements.txt'
            }
        }
        stage('Run Script') {
            steps {
                // Exécuter le script Python avec les variables d'environnement appropriées
                sh '. venv/bin/activate && python3 automatisation-rest-api.py'

            }
        }
    }

    post {
        success {
            echo 'Pipeline exécuté avec succès !'
        }
        failure {
            echo 'Le pipeline a échoué.'
        }
    }
}