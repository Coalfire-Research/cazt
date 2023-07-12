# Hierarchical IAM

Some cloud services support organizational hierarchies for management. This includes creating IAM policies at a parent level that are applied as a type of mask to descendants.

It is a mask because specifying an "Allow these APIs" at a parent level does not imply that the APIs are always or automatically allowed to a descendant. The descendant must also have a local IAM policy that allows the API call. The descendant(s) may also choose to still deny an API via their own local IAM policy.

However, if the parent specifies in the organizational policy to deny an API then its descendants cannot override the deny with an allow.

## IAM Policy

The pseudo-policy - [cazt_scen8_hierarchical.json](../../../trainee/iam_policies/cazt_scen8_hierarchical.json) contains policies demonstrating both the parent and descendant child. You should evaluate the security based on the hierarchy rules assuming that the credential profile used belongs to the descendant tenant account.

## Exercise

1. Document the result of calling each API endpoint including why you received the response you did.
1. Explain what the IAM policy stated in comparison with the result you received.
   * Why was the API endpoint vulnerable or not vulnerable?


<details>
<summary>Google Cloud Example</summary>

```
gcloud cazt get \
    --api-endpoint-overrides=https://cazt.gcloud.localtest.me:8443/uat \
    --account=cazt_scen8_hierarchical@123456789012 \
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
* Pet Sitter


## Next

Proceed to [scenario nine - HTTP 101 Switching](09-http_101_switching.md)
