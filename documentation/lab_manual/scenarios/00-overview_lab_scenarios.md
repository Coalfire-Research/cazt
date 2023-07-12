# Overview of the Lab Scenarios

## Exercise Expectations

For each scenario you will authenticate with the corresponding scenario profile with your API client. You must then test each API to verify the authorization controls were enforced. Some APIs will not be vulnerable while others will be.

1. Document the result of calling each API endpoint including why you received the response you did.
1. Explain what the IAM policy stated in comparison with the result you received.
   * Why was the API endpoint vulnerable or not vulnerable?

## API Endpoints (in-scope for testing)

The CAZT Moggy REST API has the following endpoints:
* /createmoggy
* /listMoggies
* /getMoggy
* /deletemoggy
* /RunMoggyActivity
* /petSitter

It is common to see HTTP methods associated with a REST API such as POST, PUT, PATCH, GET, DELETE. However, there is not a strict standard of adherence to using specific HTTP methods. This simulator has opted to use the POST HTTP method style for all API endpoints.

Some REST APIs pass input as URL query parameters (e.g. /someAPI?query=parameters&are=here). Other styles include placing the input values in the path of the URL. For example:
* /someAPI/moggy/MyResourceIdHere/list
* /someAPI/moggy/MyResourceIdHere
* /someAPI/moggy/MyResourceIdHere/update?someattr=newvalue

Some services offer extensive documentation of the API endpoints and their parameters. Others do not. One of the first challenges in penetration testing is determining how to call all the functionality to be tested.

This lab will not give you the detailed documentation on the API specifications, but you will be given command-line client help documentation with enough information to figure it out. If you get really stuck consider performing code review.

## Pseudo IAM Policies

In the directory [trainee/iam_policies](../../../trainee/iam_policies/) you will find a number of pseudo IAM policies that define authorization access controls for the simulator API. These are not specific in format to one cloud system but are a mash-up of multiple formats. The underlying principles for access decisions are the same.

There are no vulnerabilities in the IAM policies themselves. Instead, they define the expected authorization behavior that should be observed in a secure API. Any APIs that deviate from the policy are considered to have a security deficiency or vulnerability.

## Scenario 00 - Call Anything for Setup
The first pseudo-policy - [cazt_scen0_Setup-Any.json](../../../trainee/iam_policies/cazt_scen0_Setup-Any.json) - is intended to allow for creation of resources by the API without restriction. This allows the tester to setup necessary dependencies or resources for later test scenarios.

No vulnerability testing is expected with this policy as it should allow the API call. It is simply useful to facilitate debugging the API functionality or to assist if an unexpected error message is encountered later.

One common requirement is to create resources in multiple cloud accounts to facilitate testing cross-tenant data access later. This setup step can be performed using an expected admin role as the goal is to prepare for pen testing.


<details>
<summary>Google Cloud Example</summary>

```
# Observe that two resources are created in different tenant accounts

gcloud cazt create \
    --api-endpoint-overrides=https://cazt.gcloud.localtest.me:8443/uat \
    --account=cazt_scen1_QA_specific@000000001111 \
    --format json \
    --name=MyMoggy \
    --activity-log-object-storage=moggylitterbox-000000001111

gcloud cazt create \
    --api-endpoint-overrides=https://cazt.gcloud.localtest.me:8443/uat \
    --account=cazt_scen1_QA_specific@000000002222 \
    --format json \
    --name=NotMyMoggy \
    --activity-log-object-storage=moggylitterbox-000000002222
```

</details>

## Next

Proceed to [scenario one - QA](01-qa_specific.md)
