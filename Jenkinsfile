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
                // Installer les dépendances Python (si le script utilise des packages externes)
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run Script') {
            steps {
                // Exécuter le script Python avec les variables d'environnement appropriées
                sh '''
                python automatisation-rest-api.py 
                '''
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