import network
wlan = network.WLAN(network.STA_IF)
wlan.active(False)
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)


