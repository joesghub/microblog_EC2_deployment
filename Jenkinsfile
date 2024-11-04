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
		source venv/bin/activate
		gunicorn -b :5000 -w 4 microblog:app &
	  # Wait for Gunicorn to start
		for i in {1..10}; do
		    if nc -z localhost 5000; then
			echo "Gunicorn is up and running!"
			break
		    else
			echo "Waiting for Gunicorn to start..."
			sleep 2
		    fi
		done
	
		# Optional: Check if Gunicorn is still running after waiting
		if ! nc -z localhost 5000; then
		    echo "Gunicorn failed to start!"
		    exit 1
		fi
		'''
            }
        }
    }
}

