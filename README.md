# HA Spring Boot application deployment

The project aims to deploy a Spring Boot application in high availability model.
All the steps will be done using Infrastructure as Code.

### Features
 * DNS A record for monitoring tool and the application itself (with automation to update the record)
 * Valid SSL certificate
 * GELF drivers enabled on Docker hosts (all containers push log to Graylog)

### Notes

#### Application

 * The code 'springboot-demo-app' had to be changed because the default behaviour of the sequence generator is to increment by 50, other words, get 50 indexes up front... since we are running in HA, multiple workers cannot work with that configuration. So I changed the code accordingly.

#### Load Balancer
 * The chosen strategy for https was to use SSL Termination for convenience.
 * Although the certificate is in the repository, it is encrypted using Ansible Vault and it is decrypted during the image build.
 * All connections are blocked except those that belong to the whitelist. That's not the ideal solution. There are several ways to minimize anonymous/unwanted connections, such fine tuning the proxy based on the expected behavior (thresholds, max concurrent connections per source ip within a period of time, etc). There are also paid services that provides WAF/API Proxies. None of them will be bullet proof though.
