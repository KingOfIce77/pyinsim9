"""Example 6: Initialize InSim relay, request the host list, select
three hosts at random, then request their connection lists.

"""

import pyinsim9 as pyinsim
import random

NUMBER_HOSTS = 3

class RandomRelayPicker(object):
    def __init__(self, count):       
        # Create 'count' number relay hosts.
        for i in xrange(count):
            relay = pyinsim.relay(name='Relay %d' % (i + 1))
            relay.hosts = [] # Give each relay its own host list.
            
            # Bind events.
            relay.bind(pyinsim.IRP_HOS, self.host_list)
            relay.bind(pyinsim.IRP_ERR, self.relay_error)
            relay.bind(pyinsim.ISP_NCN, self.new_connection)
            
            # Request host list.
            relay.send(pyinsim.IRP_HLR)
            
        # Start pyinsim.
        pyinsim.run()
        
    def host_list(self, relay, hos):
        for host in hos.Info:
            # If first host, reset list.
            if host.Flags & pyinsim.HOS_FIRST:
                relay.hosts = []
                
            # Add to host list, if has conns and no spectator pass.
            # We check for > 1 cause the host itself is counted as a conn.
            if host.NumConns > 1 and not host.Flags & pyinsim.HOS_SPECPASS:
                relay.hosts.append(host)
                
            # If last host, select one.
            if host.Flags & pyinsim.HOS_LAST:
                self.select_host(relay)
                
    def select_host(self, relay):
        try:
            # Choose a random host.
            host = random.choice(relay.hosts)
        except IndexError:
            relay.close()
            print 'There are no hosts!' # Unlikely :p
        else:
            print 'Selected host: %s (%s)' % (pyinsim.stripcols(host.HName), relay.name)
            relay.send(pyinsim.IRP_SEL, HName=host.HName) # Select host.
            relay.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_NCN) # Request conns list.
            
    def relay_error(self, relay, err):
        relay.close()        
        print 'Error %d on host %s' % (err.ErrNo, relay.name)
            
    def new_connection(self, relay, ncn):
        # Print out connection name (except for host)
        if ncn.UCID:
            print 'Connection %s on host %s' % (ncn.UName, relay.name)
            
            
if __name__ == '__main__':
    # Start app, with n relay hosts.
    RandomRelayPicker(NUMBER_HOSTS)
    
    
