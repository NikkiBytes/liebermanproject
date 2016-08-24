#!/usr/bin/python

import ldap

users = []


host = 'LDAP://USCLTDC03.epri.com'
dn = 'anichollette@epri.com'
pw = 'Coc4Col444'

con = ldap.initialize(host)
con.simple_bind_s( dn, pw )

base_dn = 'ou=domain users,dc=epri,dc=com'
filter = '(objectclass=person)'
attrs = [ 'sAMAccountName'] 

list1 = con.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs) #GET LIST OF USERS W/ LDAP SEARCH FUNCTION (UGLY VERSION)
list2 = [x[1] for x in list1] #REFINE LIST1 

for x in list2:
	id = str(x.get('sAMAccountName'))
	id = id.replace("'","")
	id = id.strip('[]')
	 
	users.append(id)

with open('users.txt', 'w') as f:
	for x in users:
		if x != 'None':
			f.write(x + "\n")
	
f.close()

#powershell 
import-module activedirectory
Get-Content C:\users\pnac001\Documents\scripts\Lieberman\users.txt | Get-ADUser | select sAMAccountname, Enabled | Export-CSV C:\users\pnac001\Documents\scripts\Lieberman\AcctStat.txt