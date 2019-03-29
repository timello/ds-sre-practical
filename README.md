# HA Spring Boot application deployment

The project aims to deploy a Spring Boot application in high availability model.
All the steps will be done using Infrastructure as Code.

### Features
 * Application is built in a Docker container using the Docker builder pattern (https://docs.docker.com/develop/develop-images/multistage-build/)
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

        ansible_sudo_pass: my_sudo_password
        docker_registry: localhost:5000
        docker_internal_network: internal_nw

        postgres_password: my_postgres_password
        db_name: entries
        db_user: entries
        db_password: entries
        db_port: 5432

 3. The SSL certificate is encrypted using Ansible Vault. In order to change it and encrypt with you own key, create the file ~/.ansible_vault in the project root directory and put your key. Use the following command to encrypt the certificate PEM file:

    $ ansible-vault encrypt --vault-password-file=.ansible_vault mycertificate.pem --output=roles/haproxy/files/dschallenge.pem.vault

 4. To change the Graylog password and environment variables, please refer to the official documentation *http://docs.graylog.org/en/stable/pages/installation/docker.html*. Edit the roles/graylog/tasks/graylog.yml accordingly.

 5. Prometheus does not have password set for convenience. It should not be externally exposed though in the real environment. That can be done by configuring the HAProxy *roles/haproxy/files/haproxy.cfg* and either remove the acl from the frondend section or change the src IP accordingly.

 6. Run the command:

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

#### Considerations about performance improves, proxy redundancy, JVM metrics and overall enhancements:

 * At the proxy level, there are some ways to fine tune the HAProxy for enhancing the performance of the application such as:
  * fine tuning the max number of concurrent connections
  * increase the number of workers by setting the 'nbproc' parameter
  * CPU pin workers, that is, we can set the number of CPUs that each worker will use.
  * Adjust the load balancing algorithm to static-rr or leastconn (for long connections) (https://www.haproxy.org/download/2.0/doc/configuration.txt)

 * The proxy server can be made redundant by using DNS Load Balancing which can be implemented to check the target health during the DNS resolution.

 * Prometheus exposes through the actuator several metrics that helps throubleshooting the JVM, we can highlight the following:
  * jvm_memory_max_bytes: that can indicate that we may need to increase the allocated max heap memory for the JVM by adjusting Xmx parameter.
  * jvm_gc metrics: important to check how often the garbage collection runs and how long does it take
  * jvm_threads metrics: the more threads the more the application is working hard, that indicates something is going wrong with the application 

 * The proposed setup is using a single server for deploying application high availability. That is a simulation of a real production environment. Ideally, for containerized applications we should build a more resilient container orchestratin infrastructure like Kubernets or OpenShift. The containers should be monitored and scale automatically by setting up right probes in Kubernets/OpenShift. Also, the PODs can be distruibute among several container hosts to guarantee resilience.

 * The application development process can be setup to follow the GitOps paradigm, the CI/CD pipeline can be trigged by git pull requets/commits. We can force the applicatin to be tested prior deploying into production. Jenkins as well as other tools can be used for that.

 * The setup proposed here, uses a internal/local Docker registry. We can setup a dedicated docker registry for improving performance.
