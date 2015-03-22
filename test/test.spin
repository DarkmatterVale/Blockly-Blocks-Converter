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