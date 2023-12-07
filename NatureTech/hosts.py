from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'boer', 'NatureTech.boer_urls', name='boer'),
    host(r'boer-admin', 'NatureTech.admin_urls', name='administration'),
)