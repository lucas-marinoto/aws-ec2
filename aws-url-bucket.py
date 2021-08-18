import boto3
import pandas as pd
import os

client = boto3.client('ec2')

def group_values_list(list_temp, final_list):

    for key in list_temp:
        final_list[key] += list_temp[key]

    return final_list


def get_route_table(vpc_filter, instance_id):

    route_table = client.describe_route_tables(Filters=vpc_filter)
    route_tables = route_table['RouteTables']

    rt_infos = {
        "instance_id": [],
        "route_table_id": [],
        "destination": [],
        "target": [],
        "vpc_id": []
    }

    for rt in route_tables:

        for routes in rt['Routes']:
            rt_infos["instance_id"].append(instance_id)
            rt_infos["route_table_id"].append(rt['RouteTableId'])
            rt_infos["destination"].append(routes['DestinationCidrBlock'])
            rt_infos["target"].append(routes['GatewayId'])
            rt_infos["vpc_id"].append(rt['VpcId'])

    return rt_infos


def get_route_table_assoc_subnet(vpc_filter, instance_id):

    route_table = client.describe_route_tables(Filters=vpc_filter)
    route_tables = route_table['RouteTables']

    rt_assoc_infos = {
        "instance_id": [],
        "route_table_id": [],
        "route_table_assoc_id": [],
        "vpc_id": [],
        "subnet_id": []
    }

    for rt in route_tables:
        # rt['Associations'][0]['SubnetId']
        for assoc in rt['Associations']:
            if assoc.get('SubnetId') is not None:
                rt_assoc_infos["instance_id"].append(instance_id)
                rt_assoc_infos["route_table_id"].append(assoc['RouteTableId'])
                rt_assoc_infos["route_table_assoc_id"].append(
                    assoc['RouteTableAssociationId'])
                rt_assoc_infos["subnet_id"].append(assoc['SubnetId'])
                rt_assoc_infos["vpc_id"].append(rt['VpcId'])

    return rt_assoc_infos


def get_security_group(vpc_filter, instance_id):

    route_table = client.describe_route_tables(Filters=vpc_filter)
    route_tables = route_table['RouteTables']

    rt_assoc_infos = {
        "instance_id": [],
        "route_table_id": [],
        "route_table_assoc_id": [],
        "vpc_id": [],
        "subnet_id": []
    }

    for rt in route_tables:
        # rt['Associations'][0]['SubnetId']
        for assoc in rt['Associations']:
            if assoc.get('SubnetId') is not None:
                rt_assoc_infos["instance_id"].append(instance_id)
                rt_assoc_infos["route_table_id"].append(assoc['RouteTableId'])
                rt_assoc_infos["route_table_assoc_id"].append(
                    assoc['RouteTableAssociationId'])
                rt_assoc_infos["subnet_id"].append(assoc['SubnetId'])
                rt_assoc_infos["vpc_id"].append(rt['VpcId'])

    return rt_assoc_infos


def main():
    ec2 = boto3.resource('ec2')

    route_table = {
        "instance_id": [],
        "route_table_id": [],
        "destination": [],
        "target": [],
        "vpc_id": []
    }

    route_table_assoc_subnet = {
        "instance_id": [],
        "route_table_id": [],
        "route_table_assoc_id": [],
        "vpc_id": [],
        "subnet_id": []
    }

    instancesInfo = {
        "instance_id": [],
        "instance_type": [],
        "security_groups_name": [],
        "security_groups_id": [],
        "vpc": [],
        "subnet": [],
        "private_ip_address": [],
        "public_ip_address": []
    }

    secGroupInfos = {
        "instance_id": [],
        "vpc_id": [],
        "inboud_rules": [],
        "outbound_rules": []
    }

    for instance in ec2.instances.all():

        if instance.state['Name'] == 'running':

            vpc_filter = [
                {
                    'Name': 'vpc-id',
                    'Values': [instance.vpc_id]
                }
            ]

            for sg in instance.security_groups:
                instancesInfo["instance_id"].append(instance.id)
                instancesInfo["instance_type"].append(instance.instance_type)
                instancesInfo["vpc"].append(instance.vpc_id)
                instancesInfo["subnet"].append(instance.subnet_id)
                instancesInfo["security_groups_name"].append(sg['GroupName'])
                instancesInfo["security_groups_id"].append(sg['GroupId'])
                instancesInfo["public_ip_address"].append(
                    instance.public_ip_address)
                instancesInfo["private_ip_address"].append(
                    instance.private_ip_address)

        route_table_temp = get_route_table(vpc_filter, instance.id)
        route_table_assoc_subnet_temp = get_route_table_assoc_subnet(vpc_filter, instance.id)

        route_table = group_values_list(route_table_temp, route_table)
        route_table_assoc_subnet = group_values_list(route_table_assoc_subnet_temp, route_table_assoc_subnet)

    df_route_table = pd.DataFrame(route_table, columns=[
        'instance_id', 'route_table_id', 'destination', 'target', 'vpc_id'])

    df_route_table_assoc = pd.DataFrame(route_table_assoc_subnet, columns=[
        'instance_id', 'route_table_id', 'route_table_assoc_id', 'vpc_id', 'subnet_id'])

    df_instances = pd.DataFrame(instancesInfo, columns=[
        'instance_id', 'instance_type', 'vpc', 'subnet', 'security_groups_name', 'security_groups_id',
        'public_ip_address', 'private_ip_address'])

    with pd.ExcelWriter('ec2.xlsx', engine='xlsxwriter') as writer:
        df_instances.to_excel(writer, sheet_name='instances', index=False)
        df_route_table.to_excel(writer, sheet_name='route_table', index=False)
        df_route_table_assoc.to_excel(writer, sheet_name='route_table_assoc_subnet', index=False)

    print("## FIM ##")

main()
