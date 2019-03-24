# Uses builder pattern
FROM openjdk:8-jdk-alpine AS BUILD_IMAGE

RUN apk update && apk upgrade && \
    apk add --no-cache bash git maven ca-certificates nss procps

ENV APP_HOME=/app-src
RUN mkdir -p $APP_HOME
RUN git clone https://github.com/timello/springboot-demo-app.git $APP_HOME
WORKDIR $APP_HOME/
RUN mvn package

FROM openjdk:8-jre-alpine
WORKDIR /
COPY --from=BUILD_IMAGE /app-src/target/*.jar app.jar
VOLUME /tmp
ENTRYPOINT ["java", "-Dhibernate.id.new_generator_mappings=false", "-jar", "/app.jar"]
