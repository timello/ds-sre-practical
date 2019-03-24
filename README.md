# HA Spring Boot application deployment

The project aims to deploy a Spring Boot application in high availability model.
All the steps will be done using Infrastructure as Code.


### Notes

***The code had to be changed because the default behaviour of the sequence generator is to increment by 50, other words, get 50 indexes up front... since we are running in HA, multiple workers cannot work with that configuration. So I changed the code accordingly.***
