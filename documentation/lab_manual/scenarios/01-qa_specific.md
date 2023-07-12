# Quality Assurance Baseline (Sanity) Test

Before attempting malicious attacks against an API it is important to verify that it is actually functional and operating. 

## IAM Policy

The pseudo-policy - [cazt_scen1_QA_specific.json](../../../trainee/iam_policies/cazt_scen1_QA_specific.json) contains a list of APIs that require resources as inputs. The syntax format of these resources inside the policy is in ARN (API Resource Nomenclature) format.

You will notice that not all APIs are listed in this policy. That is because other APIs may not need any inputs (e.g. List APIs) at all. You will learn more about those in the next scenario.

The policy also contains a DependentInputResources section. This section is used to include other APIs and resources that are not in-scope for penetration testing but are required to make correct API calls. Without these policy sections you may received false results because the dependent resource access was not granted.

## Exercise

Call every API. Consult the README.md in [trainee/cloud-clients/_TYPE_/](../../../trainee/cloud-clients/) for specific client syntax examples.

1. Document the result of calling each API endpoint including why you received the response you did.
1. Were any of the APIs broken or vulnerable?


<details>
<summary>Google Cloud Example</summary>

```
gcloud cazt create \
    --api-endpoint-overrides=https://cazt.gcloud.localtest.me:8443/uat \
    --account=cazt_scen1_QA_specific@123456789012 \
    --format json \
    --name=MyMoggy \
    --activity-log-object-storage=moggylitterbox-123456789012
```

</details>

## API Endpoints (in-scope for testing)

* Create Moggy
* Get Moggy
* Delete Moggy
* Run Moggy Activity
* Pet Sitter


## Next

Proceed to [scenario one - QA Wildcard](01-qa_wildcard.md)
