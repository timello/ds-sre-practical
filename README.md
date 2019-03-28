# HA Spring Boot application deployment

The project aims to deploy a Spring Boot application in high availability model.
All the steps will be done using Infrastructure as Code.

### Features
 * DNS A record for monitoring tool and the application itself (with automation to update the record)
 * Valid SSL certificate
 * GELF drivers enabled on Docker hosts (all containers push log to Graylog)

### Quick Start

In order to deploy the application and all the stack, you need to have Ansible 2.7.5+ installed and the SSH key
exchanged with the target server host and the following steps below:

 1. Edit your local ~/.ssh/config:

        Host dsserver
          HostName <IP_TARGET_SERVER>
          User admin
          IdentityFile ~/.ssh/<SSH_PRIV_KEY>

 2. Save in the file inventory/group_vars/prod:

        ansible_become: yes
        ansible_sudo_pass: my_sudo_password
        docker_registry: localhost:5000
        docker_internal_network: internal_nw

        postgres_password: my_postgres_password
        db_name: entries
        db_user: entries
        db_password: entries
        db_port: 5432

 3. Run the command:

    $ ansible-playbook deploy.yml

### Notes

#### Server

 * Python had to be installed in the server:
    apt-get install python

#### Application

 * The code 'springboot-demo-app' had to be changed because the default behaviour of the sequence generator is to increment by 50, other words, get 50 indexes up front... since we are running in HA, multiple workers cannot work with that configuration. So I changed the code accordingly.

#### Load Balancer
 * The chosen strategy for https was to use SSL Termination for convenience.
 * Although the certificate is in the repository, it is encrypted using Ansible Vault and it is decrypted during the image build.
 * All connections are blocked except those that belong to the whitelist. That's not the ideal solution. There are several ways to minimize anonymous/unwanted connections, such fine tuning the proxy based on the expected behavior (thresholds, max concurrent connections per source ip within a period of time, etc). There are also paid services that provides WAF/API Proxies. None of them will be bullet proof though.
