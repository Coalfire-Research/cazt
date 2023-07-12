# Data Name Squatting

Object storage namespaces (a.k.a. buckets, containers, blobs) have a known abuse where they are subject to squatting. (See "S3 Bucket Namesquatting - Abusing predictable S3 bucket names" by Ian Mckay, July 31, 2019, https://onecloudplease.com/blog/s3-bucket-namesquatting).

## IAM Policy

The pseudo-policy - [cazt_scen0_Setup-Any.json](../../../trainee/iam_policies/cazt_scen0_Setup-Any.json) can be used for this exercise. You will use it for the victim tenant's calls to the APIs.

## Exercise

### Step 1

Create a new resource (CreateMoggy) with a legitimate tenant's account:

Name = `BusinessProcessUSA`

ActivityLogObjectStorage = `Our-predictable-naming-convention-USA`

### Step 2

Run the legitimate tenant's daily business process (RunMoggyActivity):

Arn = `arn:cloud:us-texas-9:`_000000000000_`:BusinessProcessUSA`

_Place the tenant's account number accordingly_

Observe the output about where the activity stored data.

### Step 3

Now consider that an attacker wishes to capture data from the victim tenant. The attacker will **not** be using the RunMoggyActivity API because they do not have the victim's credentials.

The attacker guesses that the tenant's business is going to expand their offerings into other markets. The attacker registers an object storage (in their own cloud environment) with the name
	Our-predictable-naming-convention-*ITALY*

Unobserved by the victim tenant was that ownership of this storage location did not belong to their organization.

### Step 4

The legitimate tenant creates a new resource (CreateMoggy) for their expanding business process:

Name = `BusinessProcessITALIA`

ActivityLogObjectStorage = `Our-predictable-naming-convention-ITALY`

Did you observe any security error messages?

### Step 5

Run the legitimate tenant's daily business process (RunMoggyActivity):

Arn = `arn:cloud:us-texas-9:`_000000000000_`:BusinessProcessITALIA`

_Place the tenant's account number accordingly_

Observe the output about where the activity stored data.

1.	Where would the log data be written to?
1.	Is there a security vulnerability?
1.	If so, what mitigating controls should be implemented and where?


## API Endpoints (in-scope for testing)

* Create Moggy
* Run Moggy Activity


## Next

Proceed to [scenario seven - Impersonation](07-impersonation.md)
