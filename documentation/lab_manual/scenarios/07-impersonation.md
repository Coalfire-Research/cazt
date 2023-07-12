# Impersonation

One feature of some cloud services is the ability to impersonate an IAM role or identity other than the caller of the API. This can be useful for delegating specific access controls for a reoccurring job or to a compute instance.

If an API improperly allows a user to pass an identity policy with unexpected permissions it may be possible for an attacker to escalate their privileges in the cloud environment.

## IAM Policy

The pseudo-policy - [cazt_scen7_impersonation.json](../../../trainee/iam_policies/cazt_scen7_impersonation.json) contains a policy for the PetSitter API. It is meant to restrict a legitimate caller to only providing the prescribed IAM policy. As an extra safety measure against possible future changes the tenant even added an explicit deny clause to underscore what access they did not wish to grant.

## Exercise

1. Document the result of calling each API endpoint including why you received the response you did.
1. Explain what the IAM policy stated in comparison with the result you received.
   * Why was the API endpoint vulnerable or not vulnerable?

You may assume that the attacker has knowledge of any API resource nomenclature IDs or resource names belonging to the target victim. Try providing a variety of input formats and encodings from the resources found in the policy.


<details>
<summary>Google Cloud Example</summary>

```
gcloud cazt pet-sitter \
    --api-endpoint-overrides=https://cazt.gcloud.localtest.me:8443/uat \
    --account=cazt_scen7_impersonation@123456789012 \
    --format json \
    --arn=arn:cloud:iam:us-texas-9:123456789012:FullAdmin
```

</details>

## API Endpoints (in-scope for testing)

* Pet Sitter


## Next

Proceed to [scenario eight - Hierarchical IAM](08-hierarchical_iam.md)
