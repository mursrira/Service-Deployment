# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

	for dev in service.device:
		vars = ncs.template.Variables()
		vars.add('DEVICE_NAME',dev)
        	vars.add('INTERFACE_TYPE', service.l2vpn_type.elan.interface_type)
		self.log.info("Interface Type......",service.l2vpn_type.elan.interface_type)
		vars.add('PHYS_INTF',service.l2vpn_type.elan.phys_intf)
		self.log.info("PHYS INTF",service.l2vpn_type.elan.phys_intf)
		vars.add('DOT1Q-TAG',service.l2vpn_type.elan.encapsulation)
		self.log.info("DOT1Q-TAG",service.l2vpn_type.elan.encapsulation)
		vars.add('DESCRIPTION',service.l2vpn_type.elan.description)
		self.log.info("Description ",service.l2vpn_type.elan.description)
		vars.add('BRIDGE_GROUP',service.l2vpn_type.elan.bd_group_name)
		self.log.info("Bridge Group ",service.l2vpn_type.elan.bd_group_name)
		vars.add('VFI_ID',service.l2vpn_type.elan.vfi.vfi_name)

		for peer in service.l2vpn_type.elan.vfi.neighbor:
			vars.add('DEVICE_NAME',dev)		
			vars.add('PEER_IP',peer.peer_ip)
			self.log.info("Peer IP: ",peer.peer_ip)
			vars.add('PW_ID',peer.pw_id)
			self.log.info("Psuedo Wire ID ",peer.pw_id)
			template = ncs.template.Template(service)
        		template.apply('l2vpn', vars)

    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_lock_create
    # def cb_pre_lock_create(self, tctx, root, service, proplist):
    #     self.log.info('Service plcreate(service=', service._path, ')')

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('l2vpn-servicepoint', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
