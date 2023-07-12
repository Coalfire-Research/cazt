# Same Tenant Attack

Some cloud tenants (consumers) have a security model where multiple users/groups in their own organization share a single cloud account. IAM controls allow the tenant to specify resources that some users/groups may access while others (in the same account) may not.

## IAM Policy

The pseudo-policy - [cazt_scen3_same-acct_specific.json](../../../trainee/iam_policies/cazt_scen3_same-acct_specific.json) contains a policy belonging to user A. They are restricted to only the resources in the account granted to them. Other users in the same account have their own resources for which they would have respective permission.

## Exercise

1. Document the result of calling each API endpoint including why you received the response you did.
1. Explain what the IAM policy stated in comparison with the result you received.
   * Why was the API endpoint vulnerable or not vulnerable?

The credential profile "cazt_scen0_Setup-Any" will be helpful for performing the setup steps. Use this credential to create resources belonging to "other users" in the same account that are not permissioned for user A. Example: Call Create Moggy with a "name" value of "NotForUserA" and "activity log object storage" value of "moggylitterbox-OnlyUsers"

Calling the API as user A (profile cazt_scen3_same-acct_specific) attempt to access the resources belonging to other users. You may assume that the attacker has knowledge of any API resource nomenclature IDs or resource names belonging to the target victims.


<details>
<summary>Google Cloud Example</summary>

```
gcloud cazt get \
    --api-endpoint-overrides=https://cazt.gcloud.localtest.me:8443/uat \
    --account=cazt_scen3_same-acct_specific@123456789012 \
    --format json \
    --name=NotForUserA
```

</details>

## API Endpoints (in-scope for testing)

* Create Moggy
* List Moggies
* Get Moggy
* Delete Moggy


## Next

Proceed to [scenario four - Explicit Deny](04-explicit_deny.md)
