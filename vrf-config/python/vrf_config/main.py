# -*- mode: python; python-indent: 4 -*-
import ncs
import re
from ncs.application import Service


class error(Exception):
    pass

# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------


class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        # derive RD value
        site_identifier__list = root.inventory.site_identifier__site_identifier
        node_numbers__list = root.inventory.node_numbers__node_numbers

        device = service.device

        # regex to parse siteid and node id from the device name
        regex = "(\S+?)-(\S+)\.\S+"
        m = re.match(regex, device)
        site_code = None
        node_name = None
        if m:
            site_code = m.group(1)
            node_name = m.group(2)
        else:
            raise error(
                "Unable to retrieve the site and node id for the selected device %s. Please check device name format" % device)

        site_id = site_identifier__list[site_code].rd_site_identifier
        node_id = node_numbers__list[node_name].id
        derived_rd = "2%s%s%s" % (
            site_id, node_id, str(service.route_target).zfill(5))
        
        vars = ncs.template.Variables()
        vars.add('DERIVED_RD', derived_rd)
        template = ncs.template.Template(service)
        template.apply('vrf-config-template', vars)

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
        self.register_service('vrf-config-servicepoint', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
