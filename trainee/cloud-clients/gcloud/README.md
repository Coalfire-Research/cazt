## Install

You should already have the gcloud CLI installed. You need write access to the lib folder where it is installed.

`python3 install-cazt-into-gcloud-cli.py`

## Credentials Setup

No special setup or script is required. You don't even have to log into gcloud at all as the simulator is not testing authentication but instead authorization.

For calls use the following syntax:
 _profile mode_@**account number**
 
 Examples:
 
	Tenant A: --account=cazt_scen0_Setup-Any@123456789012
	Tenant V: --account=cazt_scen5_ipaddress@000008675309

You can use `python3 setup-gcloud-cli-with-iam-test-policies.py` to get a list of possible account profiles.


## HTTP MitM Proxy Setup

`export https_proxy=http://localhost:8080/`

### Convert the Burp Suite CA certificate into PEM (Base64)
```
curl --output burp-ca.der http://localhost:8080/cert
openssl x509 -inform der -in burp-ca.der -out burp-ca.pem

gcloud config set custom_ca_certs_file `pwd`/burp-ca.pem
```

## Example client call to simulator (assumes simulator is running on same machine)

```
gcloud cazt run-activity \
    --api-endpoint-overrides=https://cazt.gcloud.localtest.me:8443/uat \
	--account=cazt_scen0_Setup-Any@123456789012 \
	--format json \
	--arn=arn:cloud:cazt:us-texas-9:123456789012:MyMoggy



gcloud cazt --help
```
