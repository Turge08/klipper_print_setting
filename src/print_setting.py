class print_setting:
    def __init__(self, config):
        self.name = config.get_name().split()[-1]
        self.printer = config.get_printer()
        self.type = config.get('type')
        self.description = config.get('description', '')
        self.value = config.get('default')
        self.gcode = self.printer.lookup_object('gcode')
        if self.type == 'bool':
            self.gcode.register_command(("DISABLE_%s" % self.name).upper(),
                self.cmd_DISABLE_SETTING,
                desc="Disable %s" % self.description)
            self.gcode.register_command(("ENABLE_%s" % self.name).upper(),
                self.cmd_ENABLE_SETTING,
                desc="Enable setting for %s" % self.description)
        self.gcode.register_mux_command("SET_SETTING", "SETTING", self.name,
            self.cmd_SET_SETTING,
            desc=self.cmd_SET_SETTING_help)
        self.printer.register_event_handler("klippy:connect",
            self.handle_connect)

    def handle_connect(self):
        variables = self.printer.lookup_object('save_variables').allVariables
        self.value = variables.get('setting_%s' % self.name, self.value)

    def cmd_DISABLE_SETTING(self, gcmd):
        self.value = False
        gcmd.respond_info("Setting %s to %s" % (self.name, self.value))
        self.gcode.run_script_from_command("SAVE_VARIABLE VARIABLE=setting_%s VALUE=%s" % (self.name, self.value))

    def cmd_ENABLE_SETTING(self, gcmd):
        self.value = True
        gcmd.respond_info("Setting %s to %s" % (self.name, self.value))
        self.gcode.run_script_from_command("SAVE_VARIABLE VARIABLE=setting_%s VALUE=%s" % (self.name, self.value))

    cmd_SET_SETTING_help = "Set Setting Value"
    def cmd_SET_SETTING(self, gcmd):
        setting_name = gcmd.get('SETTING')
        self.value = gcmd.get('VALUE')
        if self.type == 'bool':
            if self.value.upper() == 'TRUE':
                self.value = True
            else:
                self.value = False
        gcmd.respond_info("Setting %s to %s" % (setting_name, self.value))
        self.gcode.run_script_from_command("SAVE_VARIABLE VARIABLE=setting_%s VALUE=%s" % (setting_name, self.value))

    def get_status(self, eventtime):
        return {
            'value': self.value,
            'data': "{'type': '%s', 'description': '%s'}" % (self.type, self.description)
        }

def load_config_prefix(config):
    return print_setting(config)
