# Conditional Policies

One option for IAM is specifying conditional expressions that can determine whether a part of the policy is applied or not. Different cloud environments offer a number of variables and operators for these expressions. In this scenario you will be testing the ability to permit access based on a source IP address.

## IAM Policy

The pseudo-policy - [cazt_scen5_ipaddress.json](../../../trainee/iam_policies/cazt_scen5_ipaddress.json) contains an allow statement with a condition. If this condition is not met then by the rule of implicit deny no access will be granted to the CAZT APIs.

You will notice that the value of 256.256.256.256 was chosen. This is not a valid IPv4 address but was chosen for the purpose of this simulation. If the API endpoint has no vulnerabilities then the condition will never evaluate to true and thus the policy will result in no access.

## Exercise

1. Document the result of calling each API endpoint including why you received the response you did.
1. Explain what the IAM policy stated in comparison with the result you received.
   * Why was the API endpoint vulnerable or not vulnerable?

You will need to use Burp Suite (or another HTTP MitM proxy) for this exercise. First call the APIs without any tampering to verify that the expected deny occurs.

After that use Burp Suite to repeat a request with some malicious source IP spoofing HTTP headers:

```
X-Originating-IP: 256.256.256.256
X-Remote-IP: 256.256.256.256
X-Remote-Addr: 256.256.256.256
X-Client-IP: 256.256.256.256
X-Forwarded-Host: 256.256.256.256
X-Forwarded-For: 256.256.256.256
```

_This is not an exhaustive list of possibilities but is sufficient for this exercise._


<details>
<summary>Google Cloud Example</summary>

```
gcloud cazt get \
    --api-endpoint-overrides=https://cazt.gcloud.localtest.me:8443/uat \
    --account=cazt_scen5_ipaddress@123456789012 \
    --format json \
    --name=MyMoggy
```

</details>

## API Endpoints (in-scope for testing)

* Create Moggy
* List Moggies
* Get Moggy
* Delete Moggy
* Run Moggy Activity


## Next

Proceed to [scenario six - Data Name Squatting](06-data_name_squatting.md)
