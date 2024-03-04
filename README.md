# dns_app

To build an image from Dockerfile, use the following command (change the tag accordingly and notice the . at the end which specifies the context of the build):

docker build -t username/imagename:latest .

To get servers running within Docker containers communicate with each other, you can create a Docker network with the following command:

docker network create N_NAME

Once created run your containers by specifying the network name with the following command (change the parameters accordingly):

docker run --network N_NAME --name C_NAME -p 53533:53533 -it username/imagename:latest

Containers that are running within the same network should be able to communicate with each other. You can learn the IP address of your container by inspecting the network that you created with the following command:

docker inspect N_NAME
