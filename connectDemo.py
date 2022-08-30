#!/usr/bin/env python3

import boto3
import uuid

def showInstances(instances):
    for i in instances['InstanceSummaryList']:
        print("------")
        print(f"Alias: {i['InstanceAlias']}")
        print(f"\tID: {i['Arn']}")

def getInstanceByAlias(instance_list, alias):
    ix = list(filter(lambda x: x['InstanceAlias'] == alias, instance_list))
    if len(ix) == 0:
        return(None)
    else:
        return(ix[0])

def showSecurityProfiles(profile_list):
    print(f"There are {len(profile_list)} security profiles")
    for i,p in enumerate(profile_list):
        print("{i+1} ------")
        print(f"Name: {p['Name']}")
        print(f"\tArn:{p['Arn']}")

def getPermissions(client, instance_id, security_profile_id):
    permissions = client.list_security_profile_permissions( 
        InstanceId = ix['Id'],
        SecurityProfileId = profiles['SecurityProfileSummaryList'][0]['Id']
    )
    return({'security_profile_id' : security_profile_id,
            'permission_names' : permissions['Permissions']})

def randStr():
    return(str(uuid.uuid4()).split("-")[0])

if __name__ == "__main__":
    client = boto3.client('connect', region_name='us-east-1')
    print(f"AWS Connect Demo")

    instances = client.list_instances()
    print("\n\nInstances")
    showInstances(instances)

    ix = getInstanceByAlias(instances['InstanceSummaryList'], 'sjb-demo')

    ## Output the profiles
    profiles = client.list_security_profiles(InstanceId = ix['Id'])
    print("\n\nProfiles")
    showSecurityProfiles(profiles['SecurityProfileSummaryList'])

    permissions = client.list_security_profile_permissions( 
        InstanceId = ix['Id'],
        SecurityProfileId = profiles['SecurityProfileSummaryList'][0]['Id']
    )

    permissions = getPermissions(client, ix['Id'], profiles['SecurityProfileSummaryList'][3]['Id'])
    p_names = permissions['permission_names']


    report_p_names =  [
        'ReportSchedules.Create',
        'ReportSchedules.Delete',
        'ReportSchedules.Edit',
        'ReportSchedules.View']

    sp = client.create_security_profile(
        SecurityProfileName='ReportOnly' + randStr(), 
        InstanceId = ix['Id'],
        Description = 'Report Only',
        Tags = {'reporterName' : 'W. Cronkite'},
        Permissions = report_p_names
        )
    
    print(f"We just created security profile {sp['SecurityProfileArn']}.")


    ### Now, test out the search

    search_result = client.search_security_profiles(
        InstanceId = ix['Id'],
        MaxResults = 100,
        SearchCriteria = {
            "StringCondition" :  {   
                    "FieldName" : "permission",
                    "ComparisonType" : "STARTS_WITH",
                    "Value" : "ReportSchedules"
                } 
        }
    )


    search_result = client.search_security_profiles(
        InstanceId = ix['Id'],
        MaxResults = 100,
        SearchCriteria = {},
        SearchFilter = {}
    )
