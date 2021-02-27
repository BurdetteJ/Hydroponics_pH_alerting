# Components Used
This project involves a pH sensor, pH circuit, and carrier board manufactured by Atlas Scientific, as well as a Raspberry Pi microcontroller running Raspberry Pi OS. The hardware can be connected to the Pi in a few different ways, but USB was used here for convenience (the Atlas Scientific carrier board includes micro USB out).

Atlas Scientific provides some drivers, helpful sample code, and basic Raspberry Pi setup steps: https://atlas-scientific.com/files/pi_sample_code.pdf

Atlast Scientific ftdi driver:: https://github.com/Atlas-Scientific/R-pi-database-

#Objective
The goal of this project is to have the pH sensor perform continuous polling of the reservoir pH, sending out automated alerts when a pH measurement falls outside of acceptable boundaries. The user is asked to provide the following configuration values upon running the phpolling class:

**Maximum & Minimum pH**: The constitute the pH boundaries. The alert condition is any sensor measurement outside the range between these two values.
    
**Polling interval**: The amount of time to wait in between getting pH measurements from the sensor.

**Alerting interval**: The minimum interval to wait between sending out alerts. This essentially acts as a throttle, preventing a flood of messages in the event that the polling interval is short and the probe is getting measurements outside of the pH boundaries.

#Alerting Configuration
The phpolling class is intended to be as decoupled as possible from the alerting class so that the user can implement their own alerting schema as they see fit. Some common alerting techniques to consider are sms and smtp; the example alerting class here uses Twilio for sms alerting. It is worth noting that many such communications APIs come with monetary costs.