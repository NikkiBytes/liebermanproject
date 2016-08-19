

import ldap


def authenticate(address,username,password):
        '''The initialize method connects to the LDAP URL and returns
        a SimpleLDAPObject instance which is saved to a vairable.
    ---be aware initializing does not connect to the server'''

    conn = ldap.initialize('LDAP://USCLTDC04.epri.com')
    conn.protocol_version = 3 
    conn.set_option(ldap.OPT_REFERRALS, 0 )

    '''the following attempts to bind to the LDAP server
    --if an error occurs it is caught and printed to the screen'''
    try:
        result = conn.simple_bind_s(address, password)
    except ldap.INVALID_CREDENTIALS:
        return "Invalid Credentials"
        except ldap.SERVER_DOWN:
                return "The server is down."
    except ldap.LDAPError, e:
        if type(e.message) == dict and e.message.has_key('desc'):
            return "Other LDAP error: " + e.message['desc']
        else:
            return "Other LDAP error: " + e
        finally:
            conn.unbind_s()