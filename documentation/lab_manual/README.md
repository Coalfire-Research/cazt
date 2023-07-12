# Cloud AuthoriZation Trainer Lab Manual

## Prerequisites

1. Working knowledge of [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
1. Web application security penetration testing experience
1. Know the difference between authentication and authorization
1. How to use an HTTP MitM proxy tool such as Burp Suite
1. Basic knowledge of how to call REST APIs
1. Python interpreter (minimal version 3.8)

The simulator used in this lab can be run from your local machine and does not require a paid cloud service account. The lab material was tested from a Linux system, but other OSes should function in theory.

## Quick Start Setup

It is assumed that you have cloned the repository. Peaking at the source code for solutions may or may not assist you. You will still have to explain your answers to demonstrate competent knowledge and mastery of the material.

### Simulator

```
cd simulator/

bash x509/generate-self-signed.bash

python3 main_http_endpoint_server.py
```

You should see a message indicating that the simulator API service has started. It listens on port 8443 by default, but you can provide a command-line argument to change it.

### Client API Caller

1. Consult the README.md in [trainee/cloud-clients/_TYPE_/](../../trainee/cloud-clients/) for specific examples
1. Startup Burp Suite
1. Configure your API client to use the HTTP proxy
   * Usually an environment variable like `https_proxy=http://localhost:8080`
   * [proxychains](http://proxychains.net/) is another helpful tool
   * You will need to add trust to the Burp CA certification `http://localhost:8080/cert`
1. Setup the local credentials for calling the simulator APIs
   1. Consult the README.md in [trainee/cloud-clients/_TYPE_/](../../trainee/cloud-clients/)
1. Review the tenant (client API caller) IAM pseudo-policies in [trainee/iam_policies](../../trainee/iam_policies)
   * Note that editing these does not alter the simulator

## Next

Proceed to [scenario overview](./scenarios/00-overview_lab_scenarios.md)

Copyright © 2023 Coalfire.
