import boto3
from ..DnsOps import DnsOpsInterface

class AwsDnsOps(DnsOpsInterface):

    def get_hosted_zone_id(self, given_fqdn: str):
        domain = given_fqdn[given_fqdn.find('.') + 1:]

        client = boto3.client('route53')

        response = client.list_hosted_zones()

        for i in response['HostedZones']:
            if(i['Name'] == (domain + '.')):
                return i['Id'].replace('/hostedzone/', '')
                    
        return ''

    def subdomain_record(self, subdomain_name: str, reference_fqdn: str, record_type: str, request_method: str) -> dict:
    
        switcher = {
            'PUT': 'UPSERT',
            'POST': 'CREATE',
            'DELETE': 'DELETE'
        }

        action = switcher.get(request_method, 'nothing')

        hostedZoneId=self.get_hosted_zone_id(reference_fqdn)

        client = boto3.client('route53')
        domain = '.' + client.get_hosted_zone(Id=hostedZoneId)['HostedZone']['Name'][:-1]

        fqdn = subdomain_name + domain

        response = client.change_resource_record_sets(
            ChangeBatch={
                'Comment': '{} {} with {} subdomain'.format(action, fqdn, reference_fqdn),
                'Changes': [
                    {
                        'Action': action,
                        'ResourceRecordSet': {
                            'AliasTarget': {
                                'DNSName': reference_fqdn,
                                'EvaluateTargetHealth': False,
                                'HostedZoneId': hostedZoneId
                            },
                            'Name': fqdn,
                            'Type': record_type
                        },
                    },
                ],
            },
            HostedZoneId=hostedZoneId,
        )

        return response

    def healthcheck(self) -> dict:
        #check aws route53
        return {
            'healthy': True
        }