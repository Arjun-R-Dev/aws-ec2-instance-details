import boto3
import csv
ec3 = boto3.client('ec2')
regions = ec3.describe_regions().get('Regions',[] )
sts = boto3.client("sts")
account_id = sts.get_caller_identity()["Account"]
account = str(account_id)
header = ['Name', 'ID', 'Private IP', 'Type', 'Region', 'State']
f = open('%s.csv'%account_id, 'w')
writer = csv.writer(f)
writer.writerow(header)
for region in regions:
    instanceRegion=region['RegionName']
    ec2 = boto3.resource('ec2', region_name= instanceRegion)
    print("checking in region", instanceRegion)
    for instance in ec2.instances.all():
        ec2details= []
        instanceb = ec2.Instance(instance.id)
        
        #print("instance-Name :",tags["Value"])
        if (instanceb.tags) :
            for tags in instanceb.tags:
                if tags["Key"] == 'Name':
                    instanceName = tags["Value"]
        else :
            instanceName = "NoName"
        ec2details.append(instanceName)

        #print("Instance-ID : ", instance.id)
        instanceID = instance.id
        ec2details.append(instanceID)

        #print("Instance Private IP : ", instance.private_ip_address)
        instanceIP = instance.private_ip_address
        ec2details.append(instanceIP)
        
        #print("Instance-Type :", instance.instance_type)
        instanceType = instance.instance_type
        ec2details.append(instanceType)

        #print Region
        ec2details.append(instanceRegion)

        #print("Instance-State : ", instance.state.get('Name'))
        instanceState = instance.state.get('Name')
        ec2details.append(instanceState)

        writer.writerow(ec2details)
        
f.close()
