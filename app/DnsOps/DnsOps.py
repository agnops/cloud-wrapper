class DnsOpsInterface:
    def subdomain_record(self, subdomain_name: str, reference_fqdn: str, record_type: str, request_method: str) -> dict:
        return {}

    def healthcheck(self) -> dict:
        return {}