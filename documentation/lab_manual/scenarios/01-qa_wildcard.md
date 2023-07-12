# QA Baseline - Wildcards

Because the List Moggy API does not require any input parameters it does not offer the tentant customer the feature to restrict what results are returned in a listing.

Therefore, granting permission to call the List Moggies API implies that the IAM policy must use a wildcard for the resource value.

## IAM Policy

The pseudo-policy - [cazt_scen1_QA_wildcard.json](../../../trainee/iam_policies/cazt_scen1_QA_wildcard.json) contains a resource with a * in the structure. This indicates that any same-type (cazt moggy) resource may be accessed. It would have also been acceptable to use a value of "*" as the service only operates on its own resource types.

## Exercise

Call the List Moggies API. Don't forget to specify the correct credential profile (cazt_scen1_QA_wildcard).

1. Document the result of calling the API endpoint including why you received the response you did.
1. Was the API broken or vulnerable?


<details>
<summary>Google Cloud Example</summary>

```
gcloud cazt list \
    --api-endpoint-overrides=https://cazt.gcloud.localtest.me:8443/uat \
    --account=cazt_scen1_QA_wildcard@123456789012 \
    --format json
```

</details>

## API Endpoints (in-scope for testing)

* List Moggies


## Next

Proceed to [scenario two - Cross Tenant](02-cross_tenant.md)
