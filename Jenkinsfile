#!groovy​

#
# Jenkinsfile for deploying the service to the environment specified in the "environment" paremeter from the
# Jenkins pipeline configuraition.
# Assuming:
# 1. The Jenkins pipeline is configured with Git plugin and project is cloned before the script is run.
# 2. Ansible is installed together with Jenkins on the same machine (other option would be to use Ansible Tower)
# 3. Ansible inventories and playooks are available in /opt/ansible/provision-python/
# 4. Ansible roles are pre-installed on the Jenkins host machine
#

def deployToEnv(environment) {

    echo "Deploying to $environment"

    sh """

         [[ ${environment} == prod ]] && git checkout test-${BUILD_NUMBER}
         
         ansible-playbook /opt/ansible/provision-python/python-services-deploy-playbook.yaml \
                -i /opt/ansible/provision-python/inventory-${environment}.yaml \
                --extra-vars "deploy_service_name=${JOB_NAME/deploy-//}"
         
         # If this is a test deploy we need to
         [[ ${version} == test ]] && git tag release-${BUILD_NUMBER} && git push --tags
       """
}

node {  
    stage('Deployto test environment') {
        deployToEnv("test")
        sh """git tag test-${BUILD_NUMBER} && git push --tags """ 
    }
}

stage('Approval') {
    timeout(time: 360, unit: 'MINUTES') {
        userInput = input(id: 'Approval1', message: "Do you want to procceed with deployment to production?", 
            parameters: [   
                            [$class: 'BooleanParameterDefinition', defaultValue: true, description: '', 
                                        name: 'Please confirm production deploy!']
                        ]))
    }
}

node {
    stage(Deploy to production environment) {
        if ($userInput == 'true') {
            # If this is a production deploy we need to get the proper version tag, otherwise use latest master
            # Note: This is necessary because test and prod deployment nodes may not share the same work folder.
            sh """git checkout test-${BUILD_NUMBER} """
            deployToEnv("prod")
            sh """git tag release-${BUILD_NUMBER} && git push --tags """ 
            mailNotify("<list of stakeholders>")
        } else {
            echo "Skipping production deploy, pipeline was manually cancelled or time expired!"
        }
    }
}
