This file will describe the steps that need to be completed to convert any Spin code to JS code that is capable of being used in Blockly.

Code to be converted:
CON
    _clkmode        = xtal1 + pll16x
    _xinfreq        = 5_000_000

OBJ
    ctrl    : "LameControl"
    pin     : "Pinout"

CON
    LED_PIN = pin#LED
    LED_PERIOD = 10

PUB TakeControl | x

    dira[LED_PIN]~~

    repeat
        ctrl.Update

        if ctrl.A or ctrl.B or ctrl.Up or ctrl.Down or ctrl.Left or ctrl.Right
            outa[LED_PIN]~~
        else
            outa[LED_PIN]~



Code converted:
Blockly.Language.TakeControl = {
    category: 'LameStation'.
    helpUrl: '',
    init: function() {
        this.appendDummyInput( "" )
            .appendTitle( "LameStation TakeControl" );
        this.setPreviousStatement( true, null );
        this.setNextStatement( true, null );
    }
}

Blockly.spin.LameStation_Support = function() {
    Blockly.spin.definitions_[ "LameStation_ctrl" ] = 'ctrl    : "LameControl"';
    Blockly.spin.definitions_[ "LameStation_pin" ] = 'pin     : "Pinout"';
    Blockly.spin.setups_[ "LameStation_LED_PIN" ] = "LED_PIN = pin#LED";
    Blockly.spin.setups_[ "LameStation_LED_PERIOD" ] = "LED_PERIOD = 10";

    var code = "
    dira[LED_PIN]~~

    repeat
        ctrl.Update

        if ctrl.A or ctrl.B or ctrl.Up or ctrl.Down or ctrl.Left or ctrl.Right
            outa[LED_PIN]~~
        else
            outa[LED_PIN]~";
    return code;
};



Steps to be converted:
1.

2.

3.

4.

5.