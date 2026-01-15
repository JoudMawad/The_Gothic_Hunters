# Authenticacion and Authorization  

## 1. 
The passwords for users Bob and Kelly were not recovered. A brute force attack was performed for a couple of hours and because the estimated complexity of these passwords implies maybe more than 7 symbols, the time required to brute force them on this laptop could be too long. 

The recovered passwords are: 

* **eve:** eve1989
* **carol:** qwerty
* **frank:** admin
* **john:** !@#$%
* **greg:** 6666
* **norman:** c00kie
* **alice:** 12mnkys
* **dave:** alsdkfj

# Weird Service 

## a

Upon attempting to connect nc (netcat) te connection was established but inmediatly terminated, returning to the shell promt. using openssl s_client i identified that the service runs in TLS. 

However, even it was successful TLS Handshake, the server terminates the connection almost inmediatly after sending the data. This indicates a timeout for user input. The service might be designed for another type of communication, rejecting any "human" input without the correct protocol format. 

## b

The certificate is valid, there is no real authentication and i used RE to find out how the service wants to be "talked". 






