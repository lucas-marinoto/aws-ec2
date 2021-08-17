import boto3
import pandas as pd
import os

ec2 = boto3.resource('ec2')

instancesInfo = {"instance_id": [],
                 "instance_type": [],
                 "security_groups_name": [],
                 "security_groups_id": [],
                 "vpc": [],
                 "subnet": []
                 }

for instance in ec2.instances.all():

    if instance.state['Name'] == 'running':

        for sg in instance.security_groups:
            instancesInfo["instance_id"].append(instance.id)
            instancesInfo["instance_type"].append(instance.instance_type)
            instancesInfo["vpc"].append(instance.vpc)
            instancesInfo["subnet"].append(instance.subnet)
            instancesInfo["security_groups_name"].append(sg['GroupName'])
            instancesInfo["security_groups_id"].append(sg['GroupId'])

        print(
            f"Instance Id: {instance.id} || Instance Type: {instance.instance_type} || Security Group {instance.security_groups} || VPC: {instance.vpc} || Subnet: {instance.subnet}")

df = pd.DataFrame(instancesInfo, columns=[
                  'instance_id', 'instance_type', 'vpc', 'subnet', 'security_groups_name', 'security_groups_id'])
df.to_excel(r'C:\Rocketseat - React\aws-ec2\ec2.xlsx', index=False)


