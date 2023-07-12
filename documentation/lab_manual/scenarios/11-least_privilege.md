# Principle of Least Privilege

It is important that IAM policies do not grant excessive access to APIs or resources. Using the least privileges necessary reduces the risk surface of attack.

## Exercise

Answer each of the following questions:

Q1: Does the following policy follow the principle of least privilege? Why or why not?
```
[
    {
        "APIs": [
            "cazt:PetSitter",
            "iam:*"
        ],
        "Effect": "Allow",
        "Resources": [
            "arn:cloud:iam:REGION:ACCOUNTID:*"
        ]
    }
]
```

Q2: If applicable, provide a version of the policy that follows the principle of least privilege.


Q3: Does the following policy follow the principle of least privilege? Why or why not?
```
[
    {
        "APIs": [
            "cazt:GetMoggy"
        ],
        "Effect": "Allow",
        "Resources": [
            "arn:cloud:cazt:us-texas-9:123456789012:gatto",
            "arn:cloud:cazt:us-texas-9:123456789012:FelisCatus",
            "arn:cloud:cazt:us-texas-9:123456789012:FelisSilvestrisCatus"
        ]
    }
]
```

Q4: If applicable, provide a version of the policy that follows the principle of least privilege.


## Next

Proceed to [conclusion](12-conclusion.md)
