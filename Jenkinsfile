pipeline {
  agent any

  stages {
    stage('Setup venv') {
      steps {
        bat '''
        python -m venv venv
        call venv\\Scripts\\activate
        python -m pip install --upgrade pip
        pip install pytest coverage
        '''
      }
    }

    stage('Run unittest') {
      steps {
        bat '''
        call venv\\Scripts\\activate
        python -m unittest discover -s tests -p "test_*.py"
        '''
      }
    }

    stage('Run pytest + coverage') {
      steps {
        bat '''
        call venv\\Scripts\\activate
        coverage run -m pytest --junitxml=tests\\test-results.xml
        coverage report -m
        coverage html
        coverage xml -o coverage.xml
        '''
      }
    }
  }

  post {
    always {
      junit 'tests\\test-results.xml'

      publishHTML(target: [
        reportDir: 'htmlcov',
        reportFiles: 'index.html',
        reportName: 'Coverage Report',
        keepAll: true
      ])

      recordCoverage(tools: [cobertura(pattern: 'coverage.xml')])
    }
  }
}
