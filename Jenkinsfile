pipeline {
 agent any
    stages {
        stage ('Build') {
            steps {
                sh '''#!/bin/bash
                python3.9 -m venv venv
            	source venv/bin/activate
            	pip install pip --upgrade
            	pip install -r requirements.txt
            	pip install gunicorn pymysql cryptography
           	FLASK_APP=microblog.py
            	flask translate compile
            	flask db upgrade
                '''
            }
        }
        stage ('Test') {
            steps {
                sh '''#!/bin/bash
                source venv/bin/activate
		export PYTHONPATH=$(pwd)
		py.test ./tests/unit/ --verbose --junit-xml test-reports/results.xml
                '''
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
      stage ('OWASP FS SCAN') {
    steps {
        script {
            try {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
            } catch (Exception e) {
                echo "OWASP FS SCAN failed: ${e.message}"
                currentBuild.result = 'UNSTABLE'
            }
        }
        dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
    }
}
      stage ('Clean') {
            steps {
                sh '''#!/bin/bash
                if [[ $(ps aux | grep -i "gunicorn" | tr -s " " | head -n 1 | cut -d " " -f 2) != 0 ]]
                then
                ps aux | grep -i "gunicorn" | tr -s " " | head -n 1 | cut -d " " -f 2 > pid.txt
                kill $(cat pid.txt)
                exit 0
                fi
                '''
            }
        }
      stage ('Deploy') {
            steps {
                sh '''#!/bin/bash
		# Activate the virtual environment
		source /home/ubuntu/jenkins/microblog_EC2_deployment/myenv/bin/activate
	
		# Restart the Gunicorn service
		sudo systemctl restart gunicorn
	
		# Check if Gunicorn restarted successfully
		if sudo /bin/systemctl is-active --quiet gunicorn; then
		    echo "Gunicorn restarted successfully"
		else
		    echo "Failed to restart Gunicorn"
		    # Print logs for debugging
		    sudo /bin/journalctl -u gunicorn.service --since "5 minutes ago"
		    exit 1
		fi
            }
        }
    }
}

