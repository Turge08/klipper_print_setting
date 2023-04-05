# Klipper Print Setting

## ** CURRENTLY IN BETA **

## Introduction:

This is an add-on to Klipper for creating persistent "print settings" that can be modified/toggled on-the-fly. These print setting can be used in various macros. 

If/when this gets merged into klipper, it's my hope that the Fluidd/Mainsail devs will add a section to the Dashboard so that these settings can be toggled/changed through the click of a button.

## Sample Usage:

You have a nozzle brush. In your print_start macro, "clean_nozzle" instructs to clean the nozzle before every print. For whatever reason, you want to disable this.

Normally, you would need to edit your printer.cfg, comment out "clean_nozzle" in the print_start macro and restart the firmware.

With a clean_nozzle print setting, you would simply run the "DISABLE_CLEAN_NOZZLE" gcode.

To set this up, you would:

- Add a new print setting to your printer.cfg:

<pre>[print_setting clean_nozzle]
description: Clean nozzle before print
default: False
type: bool</pre>

- Replace "Clean_Nozzle" in your print_start macro with the following:

<pre>{% if printer["print_setting clean_nozzle"].value == true %}
  Clean_Nozzle
{% endif %}</pre>

You now have 3 gcode commands to toggle the clean nozzle function:

<pre>DISABLE_CLEAN_NOZZLE
ENABLE_CLEAN_NOZZLE
SET_SETTING SETTING=clean_nozzle VALUE=False</pre>

Here are some examples of some print settings I use:

<pre>[print_setting print_area_x]
description: Maximum print area width
default: 250
type: float

[print_setting print_area_y]
description: Maximum print area depth
default: 250
type: float

[print_setting bed_mesh]
description: Perform bed mesh before print
default: False
type: bool

[print_setting prime_line]
description: Perform prime line before print
default: False
type: bool

[print_setting clean_nozzle]
description: Clean nozzle before print
default: False
type: bool

[print_setting bed_level]
description: Perform bed level before print
default: False
type: bool

[print_setting default_bed_mesh]
description: Load default bed mesh on startup
default: False
type: bool

[print_setting bed_mesh_by_temp]
description: Load bed mesh if name matches target bed temperature
default: False
type: bool

[print_setting adaptive_bed_mesh]
description: Perform adaptive bed mesh based on print size
default: True
type: bool

[print_setting home_z]
description: Home Z before print
default: False
type: bool

[print_setting calibrate_z]
description: Calibrate Z before print
default: False
type: bool

[print_setting center_before_print]
description: Center nozzle before print
default: False
type: bool

[print_setting end_retraction_length]
description: Retraction length on print cancel/end
default: 10
type: float</pre>

It's important to note that without making the required changes to the macros, the settings above won't do anything.

## Install

<pre>cd ~
git clone https://github.com/Turge08/klipper_print_setting
cd klipper_print_setting
./install.sh</pre>

## Requirements

To make these changes persistent across a firmware/host restart, this feature also requires the presence of [save_variables] to be added to your printer.cfg. If you already have save_variables from running ERCF (Enraged Rabbit Carrot Feeder) for example, then the current cfg file will be used to save the persistent print settings. You can really only have 1 [save_variables] entry.

<pre>[save_variables]
filename: ~/klipper_config/saved_variables.cfg</pre>

## Optional:

To view all current print settings, you can simply open the "saved_variables.cfg" file. You can also use the following macro:

<pre>[gcode_macro List_Print_Settings]
gcode:
    { action_respond_info("************************") }
    { action_respond_info("*** PRINT SETTINGS ***") }
    { action_respond_info("************************") }
    {% for name in printer %}
        {% if name.startswith('print_setting') %}
            { action_respond_info("%s: %s" % (name.replace('print_setting ', ''), printer[name].value)) }
        {% endif %}
    {% endfor %}
    { action_respond_info("************************") }</pre>
    
Sample Output:

<pre>************************
*** PRINT SETTINGS ***
************************
print_area_x: 250
print_area_y: 210
bed_mesh: False
prime_line: False
clean_nozzle: False
bed_level: True
default_bed_mesh: False
bed_mesh_by_temp: True
adaptive_bed_mesh: True
home_z: True
calibrate_z: False
center_before_print: True
end_retraction_length: 20
************************</pre>

New GCode Commands:

Simply typing "Help" in the Console will list all commands. You'll find the toggle commands that start with "DISABLE" or "ENABLE":

<pre>// DISABLE_BED_LEVEL: Disable Perform bed level before print
// DISABLE_BED_MESH: Disable Perform bed mesh before print
// DISABLE_BED_MESH_BY_TEMP: Disable Load bed mesh if name matches target bed temperature
// DISABLE_CALIBRATE_Z: Disable Calibrate Z before print
// DISABLE_CENTER_BEFORE_PRINT: Disable Center nozzle before print
// DISABLE_CLEAN_NOZZLE: Disable Clean nozzle before print
// DISABLE_DEFAULT_BED_MESH: Disable Load default bed mesh on startup
// DISABLE_HOME_Z: Disable Home Z before print
// DISABLE_PRIME_LINE: Disable Perform prime line before print
// ENABLE_ADAPTIVE_BED_MESH: Enable setting for Perform adaptive bed mesh based on print size
// ENABLE_BED_LEVEL: Enable setting for Perform bed level before print
// ENABLE_BED_MESH: Enable setting for Perform bed mesh before print
// ENABLE_BED_MESH_BY_TEMP: Enable setting for Load bed mesh if name matches target bed temperature
// ENABLE_CALIBRATE_Z: Enable setting for Calibrate Z before print
// ENABLE_CENTER_BEFORE_PRINT: Enable setting for Center nozzle before print
// ENABLE_CLEAN_NOZZLE: Enable setting for Clean nozzle before print
// ENABLE_DEFAULT_BED_MESH: Enable setting for Load default bed mesh on startup
// ENABLE_HOME_Z: Enable setting for Home Z before print
// ENABLE_PRIME_LINE: Enable setting for Perform prime line before print</pre>
    
