#!groovy​

#
# Jenkinsfile for deploying the service to the environment specified in the "environment" paremeter from the
# Jenkins pipeline configuraition.
# Assuming:
# 1. The Jenkins pipeline is configured with Git plugin and environment parameter.
# 2. Ansible is installed together with Jenkins on the same machine (other option would be to use Ansible Tower)
# 3. Assuming Ansible inventories and playooks are available in /opt/ansible/provision-python/
# 4. Ansible roles are pre-installed on the Jenkins host machine
#

node {
    
    stage('Deploy') {
        sh """
             ansible-playbook /opt/ansible/provision-python/python-services-deploy-playbook.yaml \
             -i /opt/ansible/provision-python/inventory-${params.environment}.yaml \
             --extra-vars "deploy_service_name"  
           """
    }
}
