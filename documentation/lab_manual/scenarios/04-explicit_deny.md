# Explicit Deny

Another basic IAM policy feature is the ability to deny access. An explicit deny should override any allows.

## IAM Policy

The pseudo-policy - [cazt_scen4_explicit-deny.json](../../../trainee/iam_policies/cazt_scen4_explicit-deny.json) contains a policy where each CAZT API is allowed but later denied.

## Exercise

1. Document the result of calling each API endpoint including why you received the response you did.
1. Explain what the IAM policy stated in comparison with the result you received.
   * Why was the API endpoint vulnerable or not vulnerable?


<details>
<summary>Google Cloud Example</summary>

```
gcloud cazt get \
    --api-endpoint-overrides=https://cazt.gcloud.localtest.me:8443/uat \
    --account=cazt_scen4_explicit-deny@123456789012 \
    --format json \
    --name=AnyNameHere
```

</details>

## API Endpoints (in-scope for testing)

* Create Moggy
* List Moggies
* Get Moggy
* Delete Moggy
* Run Moggy Activity
* Pet Sitter


## Next

Proceed to [scenario four - Implicit Deny](04-implicit_deny.md)
