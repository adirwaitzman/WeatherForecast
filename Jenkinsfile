pipeline {
    agent { 
        node {
            label 'agent1'
        }
    }

    stages {
        stage('Build Docker Image') {
            steps {
                // Build the Docker image               
                sh 'docker build -t weatherapp .'
                slackSend color: "#00FF00", message: "${env.JOB_NAME} ${env.BUILD_NUMBER} job (<${env.BUILD_URL}|Open>) - Build Docker Image stage completed successfully."         
            }
        }
        stage('Test') {
            steps {
                script{
                    try {
                        sh 'python3 ./Weather_Forecast-testuint.py'
                        slackSend color: "#00FF00",  message: "${env.JOB_NAME} ${env.BUILD_NUMBER} job (<${env.BUILD_URL}|Open>) - Test stage completed successfully."
                    } catch (Exception e) {
                        slackSend color: "#FF0000",  message: "${env.JOB_NAME} ${env.BUILD_NUMBER} job (<${env.BUILD_URL}|Open>) - Test stage failed."
                        error("Test stage failed.")
                    }
                }
            }
        }
        stage('Push Docker Image') {
            steps {            
                sh 'docker tag weatherapp adirwaitzman/weatherapp'            	
                sh 'docker image push adirwaitzman/weatherapp'
                slackSend color: "#439FE0",  message: "${env.JOB_NAME} ${env.BUILD_NUMBER} job (<${env.BUILD_URL}|Open>) - tPush Docker Image stage completed successfully."
            }
        }
        stage('Deploy') {
            steps {
                sshagent (credentials: ['WeatherForecast-production']) {            	
                    sh "ssh -o StrictHostKeyChecking=no ubuntu@172.31.33.29 'docker compose pull'"
                    sh "ssh -o StrictHostKeyChecking=no ubuntu@172.31.33.29 'docker compose up -d'"
                }
            }           	
        }
    }
}

