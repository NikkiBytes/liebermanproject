#!/usr/bin/python

import ldap

host = 'LDAP://USCLTDC03.epri.com'
dn = 'anichollette@epri.com'
pw = 'Coc4Col444'



con = ldap.initialize(host)
con.simple_bind_s( dn, pw )


base_dn = 'ou=domain users,dc=epri,dc=com'
filter = '(objectclass=person)'
attrs = ['firstname', 'lastname', 'compID']

con.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs)
