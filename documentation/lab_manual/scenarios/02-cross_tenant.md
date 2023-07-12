# Cross Tenant Attack

An important part of access control is not allowing one tenant to access the data of another without their permission. In cloud environments the impact of such a vulnerability would undermine the entire premise of the shared system.

## IAM Policy

The pseudo-policy - [cazt_scen2_cross-tenant.json](../../../trainee/iam_policies/cazt_scen2_cross-tenant.json) contains a policy that an attacker would install into their own account. The attacker's goal is to call any API with malicious inputs that deceive it into disclosing another tenant's data to them. Therefore, the attacker grants (their own account) broad access permissions in the policy.

Notice the multiple values provided for the Resources element. These indicate targets that the attacker wishes to access without legitimate authorization. A correct API will not provide access to another tenant's data just because the attacker's own IAM policy lists it.

## Exercise

1. Document the result of calling each API endpoint including why you received the response you did.
1. Explain what the IAM policy stated in comparison with the result you received.
   * Why was the API endpoint vulnerable or not vulnerable?

Using a legitimate tenant (target victim) account credential profile create some moggy resources. These will be the desired target of the attacker. The credential profile cazt_scen0_Setup-Any can be used for creation calls.

You will need a second tenant account credential profile (cazt_scen2_cross-tenant) for the attacker API calls.

You may assume that the attacker has knowledge of any API resource nomenclature (ARNs) or resource names belonging to the target victim. Try providing a variety of input formats and encodings. Some examples:
* SomeResourceNameOnly
* `arn:cloud:cazt:REGION:ACCOUNTID:SomeResourceNameOnly`
  * `arn:cloud:cazt:us-texas-9:123456789012:SomeResourceName`
* `arn:cloud:cazt:us-texas-9:123456789012:SomeResource%4E%61%6D%65`
  * URL encoding
* `arn:cloud:caZt:us-TeXas-9:123456789012:SomeResourceName`
  * Case sensitivity


<details>
<summary>Google Cloud Example</summary>

```
gcloud cazt get \
    --api-endpoint-overrides=https://cazt.gcloud.localtest.me:8443/uat \
    --account=cazt_scen2_cross-tenant@123456789012 \
    --format json \
    --name=NotMyMoggy
```

</details>

## API Endpoints (in-scope for testing)

* Create Moggy
* List Moggies
* Get Moggy
* Delete Moggy
* Run Moggy Activity


## Next

Proceed to [scenario three - Same Account Attack](03-same_account.md)
