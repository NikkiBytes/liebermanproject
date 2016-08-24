#!/usr/bin/python

#must have python-ldap installed
import ldap 

active = []
users = []
computers = []
userComp = []
activeUsers = []



host = 'LDAP://USCLTDC03.epri.com'
dn = 'anichollette@epri.com'
pw = 'Coc4Col444'




con = ldap.initialize(host)
con.simple_bind_s( dn, pw )


#SEARCH FOR USERS 

base_dn = 'ou=domain users,dc=epri,dc=com'
filter = '(objectclass=person)'
attrs = ['givenName', 'sn', 'sAMAccountName'] #first name, last name, logonID

list1 = con.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs) 
list2 = [x[1] for x in list1]  


for x in list2:
	fn = str(x.get('givenName')) 
	fn = fn.replace("'","")
	fn = fn.strip('[]')

	ln = str(x.get('sn'))
	ln = ln.replace("'","")
	ln = ln.strip('[]')

	id = str(x.get('sAMAccountName'))
	id = id.replace("'","")
	id = id.strip('[]')
	
	n = [fn, ln]
	n = " ".join(n)

	t = [fn, ln, id, n]
	users.append(t)


#SEARCH FOR COMPUTERS

base_dn = 'ou=domain computers,dc=epri,dc=com'  
attrs = ['cn', 'description']

compList = con.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs) 
compList2 = [x[1] for x in compList] 


#REFINE COMPUTER LIST

for x in compList2:
	cn = str(x.get('cn'))
	cn = cn.replace("'","")
	cn = cn.strip('[]')

	des = str(x.get('description'))
	des = des.replace("'","")
	des = des.strip('[]')

	t = [cn, des]
	computers.append(t) 



with open('AcctStat.txt', 'r') as f: 
	for l in f:
		if not l.startswith("#") and not l.startswith("sAMAccountname"):
			l = l.replace('"','')
			a = l.split(',')[0]
			b = l.split(',')[1]
			b = b.strip('\n')
			if b == 'True':
				z = [a,b]
				active.append(z)
f.close()

#REFINE USER LIST

	


#MATCH COMPUTER W/ USER
#ADD MORE FILTER HERE



for a in users:
	for b in active:
		if a[2] == b[0]:
			x = [a[2], a[3]]
			activeUsers.append(x)


for x in computers:
	for v in activeUsers:
		if v[1] in x[1]:
			y = [v[0], x[0]]
			userComp.append(y)

			
	


#OPEN/WRITE TO TEXT FILE

fA ='PermissionsOnSystems.txt'
fB = 'DelegationIdentitiesPermissionsAndManagementSets.txt'

with open(fA, 'w') as f1:
	#FORMAT FINAL OUTPUT 
	#EDIT FORMAT FOR FINAL 
	for x in userComp:
		if x[1] != 'None':
			string = ('EPRI\\'+x[0]+','+x[1]+',524290,1')
			f1.write(string + "\n")
with open(fB, 'w') as f2:
	for x in userComp:
		if x[1] != 'None':
			string = ('EPRI\\'+x[0]+',1,,65537,')
			f2.write(string + "\n")


f1.close()
f2.close()
