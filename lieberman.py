#!/usr/bin/python

#must have python-ldap installed
import ldap 

active = []
users = []

computers = []
userComp = []

#RELEVANT CREDENTIALS

host = 'LDAP://USCLTDC03.epri.com'
dn = 'xxxxx'
pw = 'xxxxxx'


#CONNECT TO LDAP SERVER

con = ldap.initialize(host)
con.simple_bind_s( dn, pw )


#SEARCH FOR USERS 

base_dn = 'ou=domain users,dc=epri,dc=com'
filter = '(objectclass=person)'
attrs = ['givenName', 'sn', 'sAMAccountName'] #first name, last name, logonID

list1 = con.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs) #GET LIST OF USERS W/ LDAP SEARCH FUNCTION (UGLY VERSION)
list2 = [x[1] for x in list1] #REFINE LIST1 


#SEARCH FOR COMPUTERS

base_dn = 'ou=domain computers,dc=epri,dc=com'  
attrs = ['cn', 'description']

compList = con.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs) #ugly compList
compList2 = [x[1] for x in compList] #refined compList w/ CN, description


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

#REFINE USER LIST
#USER LIST CONTAINS givenName, sn, accountID 

#IDEA- CAN I CALL getUserFile.py TO REDUCE COMPLEXITY

	
for x in list2:
	fn = str(x.get('givenName')) #convert to string 
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
	
	
#FINAL LIST (first_name, last_name, acctID, 'description'[fn,ln])
	
with open('usersID.txt', 'w') as f:
	for x in users:
		id = x.split(',')[2]
			if id != none:
				f.write(id + '\n')

f.close()

# RUN POWERSHELL COMMAND TO FIND ACTIVE USERS#'sub logic', equivalent of a table				
Get-Content C:\users\pnac001\Documents\scripts\Lieberman\usersID.txt | Get-ADUser | select sAMAccountname, Enabled | Export-CSV C:\users\pnac001\Documents\scripts\Lieberman\AcctStat.txt
	
	
	
##############################################################

#MATCH COMPUTER W/ USER
#MUST HAVE FILE FROM POWERSHELL COMMAND ('AcctStat.txt')


with open('AcctStat.txt', 'r') as f: 
	for l in f:
		if not l.startswith("#") and not l.startswith("sAMAccountname"):
			l = l.replace('"','')
			a = l.split(',')
			b = l.split(',')
			z = [a,b]
			active.append(z)
f.close()




for x in computers:
	for v in usersA:
		acctName = v[3]
		acctN = x[1]
		for z in active:
			if acctName in acctN:
				if acctName in z[0] and z[1] == 'True'
					z = [x[0], v[2], v[3], z[1]] 
					userComp.append(z)
 		


#OPEN/WRITE TO TEXT FILE

fA ='PermissionsOnSystems.txt'
fB = 'DelegationIdentitiesPermissionsAndManagementSets.txt'

with open(fA, 'w') as f1:
	#FORMAT FINAL OUTPUT 
	#EDIT FORMAT FOR FINAL 
	for x in userComp:
		if x[1] != 'None':
			string = ('EPRI\\'+x[1]+','+x[0]+',524290,1')
			f1.write(string + "\n")
with open(fB, 'w') as f2:
	for x in userComp:
		if x[1] != 'None':
			string = ('EPRI\\'+x[1]+',1,,65537,')
			f2.write(string + "\n")


f1.close()
f2.close()