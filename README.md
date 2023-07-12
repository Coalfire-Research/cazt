CAZT (Cloud AuthoriZation Trainer) is a simulator of cloud-provider responsible REST APIs. It includes a lab manual for getting hands-on practice with how to attack authorization vulnerabilities in a cloud API.

It is different from other vulnerable cloud practice environments because it focuses on the cloud-provider shared responsibility instead of the customer. This enables pen testers to gain experience with testing the cloud vendor itself as well as an understanding of what a vulnerable cloud service will look like.

### Features

* Interface for using cloud-provider command-line interfaces to practice
* A lab manual with OWASP authorization vulnerability scenarios
* Six API endpoints for vulnerability discovery

### Requirements

* The simulator and pen test tools can be run from a single local machine
* Fundamental knowledge of HTTP proxy MitM tools (i.e. Burp)
* Basic experience with using a command-line
* Basic experience with using a cloud-provider's command-line interface tool

#### Platforms

Development and testing was done under Ubuntu Linux, but other platforms with at least Python 3.8 should be compatible as well.

### Install

Clone the repository using git.

Install the required packages using pip3.

``` bash
sudo apt install -y python3-virtualenv python3-pip

virtualenv -p python3 venv
source venv/bin/activate

pip3 install -r requirements.txt
```

### Lab Manual

Proceed to [documentation/lab_manual/](documentation/lab_manual/)

----

![](documentation/images/bhusa2023-arsenal-badge.svg?raw=true)

https://www.blackhat.com/us-23/arsenal/schedule/presenters.html#rodney-beede-45501
