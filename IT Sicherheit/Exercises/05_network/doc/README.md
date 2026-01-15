# Basic Network Security 

## 1.- traffic.dump

### (a) 
* **SMPT**
* **FTP**
* **TELNET**

### (b) 
* **AqEwoPJN**

### (c) 
* **marlyy@zeno.eyrie.af.mil**
* **akirah@swallow.eyrie.af.mil** 

### (d) 
* IP: 194.7.248.153

## 2.- 
 ### (a) UDP:
 Is possible, because UDP is a connectionless protocol. It does not require a handshake to beggin data transmission, similar to ICMP. 
 An attacker can perform IP spoofing by forging the IP adress of the victim as the source of a UDP packet sent to a broadcast adress. If the target network has services like "echo" emabled, all hosts in the subnet will send their responses to the victim and causing a denial of service condition. 

 ### (b) TCP 
 Not possible, because TCP is connection oriented proctocol that relies o the three way handshake to establish communication. 
 if an attacker sends a SYN packet with a spoofed source IP (the victims ip), the server will respond with a SYN-ACK to the victim, not the attacker and the attacker will not be able to send the final ACK to complete the connection.
 