docker build --build-arg CONFIGCAT_AUTH_KEY=yourkeyhere --build-arg JOB_ID=1234 -t myreactapp .
docker run -p 3000:3000 -e JOB_ID=1234 myreactapp
