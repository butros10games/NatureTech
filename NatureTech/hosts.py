from django_hosts import host, patterns

host_patterns = patterns(
    "",
    host(r"boer", "NatureTech.boer_urls", name="boer"),
    host(r"boer-admin", "NatureTech.admin_urls", name="administration"),
)
