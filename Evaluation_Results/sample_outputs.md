# Sample outputs with citations

### Q1. Which AUTOSAR platform and release does the BCM use?
- Expected: AUTOSAR Classic Platform R21-11 (pages [2])
- System answer: Section: 1. Introduction and Scope
This document describes the high-level design of the Body Control Module (BCM). The BCM controls
the central door locks, the power windows and the exterior lighting of the vehicle.
The BCM software is built on the AUTOSAR Classic Platform, release R21-11. The application layer
contains five software components: DoorLockManager, WindowControl, LightingController,
PowerModeManager and BcmDiagnostics.
Out of scope for this release: wipers, climate control (HVAC) and passive keyless entry. [Page 2]
- Cited pages: [2] | Retrieved pages: [2, 1, 8, 7] | Top distance: 0.225 | Mode: extractive
- Correct: True

### Q2. How many software components are in the application layer?
- Expected: Five (pages [2, 3])
- System answer: Section: 2. Architecture Overview
The software is organised in layers: the application layer with five software components, the Runtime
Environment (RTE), the Basic Software (BSW) services (Com, NvM, Dem, Dcm), the ECU
abstraction layer and the microcontroller abstraction layer (MCAL).
The BCM is connected to the body CAN bus at 500 kbit/s. The window switches are connected over
LIN at 19.2 kbit/s.
Component Type Runnable period Owner team
DoorLockManager Application SWC 10 ms Body Team A
WindowControl Application SWC 20 ms Body Team B
LightingController Application SWC 50 ms Lighting Team
PowerModeManager Service SWC 10 ms Platform Team
BcmDiagnostics Application SWC 100 ms Diagnostics Team [Page 3]
- Cited pages: [3] | Retrieved pages: [3, 12, 8, 2] | Top distance: 0.227 | Mode: extractive
- Correct: True

### Q3. What is the runnable period of DoorLockManager?
- Expected: 10 ms (pages [3, 4])
- System answer: Section: 3.1 DoorLockManager
DoorLockManager locks and unlocks the four doors. It handles central-locking requests, automatic
locking while driving and crash unlock.
Its runnable DoorLock_Run10ms executes every 10 ms. The lock actuators are driven through a Dio
channel group.
Crash unlock: when the signal CrashDetected is set to 1 by the airbag control unit, DoorLockManager
unlocks all doors within 100 ms.
Auto-lock: when VehicleSpeed is above 10 km/h, all doors are locked automatically.
The last lock state is stored in the NvM block NvM_DoorLockState so it survives a power cycle. [Page 4]
- Cited pages: [4] | Retrieved pages: [4, 10, 12, 5] | Top distance: 0.192 | Mode: extractive
- Correct: True

### Q4. Which team owns LightingController?
- Expected: Lighting Team (pages [3])
- System answer: Not found in the document.
- Cited pages: [] | Retrieved pages: [6, 14, 3, 13] | Top distance: 0.407 | Mode: threshold-refusal
- Correct: False

### Q5. What bit rate does the body CAN bus use?
- Expected: 500 kbit/s (pages [3, 9])
- System answer: Section: 5. CAN Signals and Messages
All messages below are on the body CAN bus at 500 kbit/s.
Signal Message CAN ID Direction Cycle
VehicleSpeed ESC_Status 0x1A0 Rx 20 ms
CrashDetected ACU_Crash 0x0C5 Rx Event-triggered
IgnitionState IGN_Status 0x120 Rx 50 ms
DoorLockStatus BCM_Body1 0x3B0 Tx 100 ms
WindowPos_FL BCM_Window 0x3B8 Tx 100 ms
HeadlampState BCM_Light 0x3C0 Tx 200 ms [Page 9]
- Cited pages: [9] | Retrieved pages: [9, 3, 1, 12] | Top distance: 0.287 | Mode: extractive
- Correct: True

### Q6. What does DoorLockManager do when CrashDetected is set?
- Expected: Unlocks all doors within 100 ms (pages [4])
- System answer: Section: 3.1 DoorLockManager
DoorLockManager locks and unlocks the four doors. It handles central-locking requests, automatic
locking while driving and crash unlock.
Its runnable DoorLock_Run10ms executes every 10 ms. The lock actuators are driven through a Dio
channel group.
Crash unlock: when the signal CrashDetected is set to 1 by the airbag control unit, DoorLockManager
unlocks all doors within 100 ms.
Auto-lock: when VehicleSpeed is above 10 km/h, all doors are locked automatically.
The last lock state is stored in the NvM block NvM_DoorLockState so it survives a power cycle. [Page 4]
- Cited pages: [4] | Retrieved pages: [4, 10, 12, 13] | Top distance: 0.197 | Mode: extractive
- Correct: True

### Q7. At what vehicle speed are the doors locked automatically?
- Expected: Above 10 km/h (pages [4])
- System answer: Section: 3.1 DoorLockManager
DoorLockManager locks and unlocks the four doors. It handles central-locking requests, automatic
locking while driving and crash unlock.
Its runnable DoorLock_Run10ms executes every 10 ms. The lock actuators are driven through a Dio
channel group.
Crash unlock: when the signal CrashDetected is set to 1 by the airbag control unit, DoorLockManager
unlocks all doors within 100 ms.
Auto-lock: when VehicleSpeed is above 10 km/h, all doors are locked automatically.
The last lock state is stored in the NvM block NvM_DoorLockState so it survives a power cycle. [Page 4]
- Cited pages: [4] | Retrieved pages: [4, 5, 10, 2] | Top distance: 0.25 | Mode: extractive
- Correct: True

### Q8. Which NvM block stores the door lock state?
- Expected: NvM_DoorLockState (pages [4, 12])
- System answer: Section: 3.1 DoorLockManager
DoorLockManager locks and unlocks the four doors. It handles central-locking requests, automatic
locking while driving and crash unlock.
Its runnable DoorLock_Run10ms executes every 10 ms. The lock actuators are driven through a Dio
channel group.
Crash unlock: when the signal CrashDetected is set to 1 by the airbag control unit, DoorLockManager
unlocks all doors within 100 ms.
Auto-lock: when VehicleSpeed is above 10 km/h, all doors are locked automatically.
The last lock state is stored in the NvM block NvM_DoorLockState so it survives a power cycle. [Page 4]
- Cited pages: [4] | Retrieved pages: [4, 10, 12, 2] | Top distance: 0.307 | Mode: extractive
- Correct: True

### Q9. How long does the window motor reverse after anti-pinch detection?
- Expected: 200 ms (pages [5])
- System answer: Section: 3.2 WindowControl
WindowControl drives the four window motors. It supports manual up/down and one-touch up/down.
Its runnable executes every 20 ms.
Anti-pinch: during one-touch close, an obstruction is detected from the motor current. On detection
the motor is reversed for 200 ms.
The maximum one-touch travel time is 4 seconds.
Window operation is disabled when the battery voltage is below 9 V, to protect the battery.
The window switch inputs arrive over LIN from the door switch pods. [Page 5]
- Cited pages: [5] | Retrieved pages: [5, 14, 6, 13] | Top distance: 0.212 | Mode: extractive
- Correct: True

### Q10. Below which battery voltage is window operation disabled?
- Expected: 9 V (pages [5])
- System answer: Section: 3.2 WindowControl
WindowControl drives the four window motors. It supports manual up/down and one-touch up/down.
Its runnable executes every 20 ms.
Anti-pinch: during one-touch close, an obstruction is detected from the motor current. On detection
the motor is reversed for 200 ms.
The maximum one-touch travel time is 4 seconds.
Window operation is disabled when the battery voltage is below 9 V, to protect the battery.
The window switch inputs arrive over LIN from the door switch pods. [Page 5]
- Cited pages: [5] | Retrieved pages: [5, 14, 7, 12] | Top distance: 0.284 | Mode: extractive
- Correct: True

### Q11. What are the lux thresholds for automatic headlights?
- Expected: On below 400 lux, off above 800 lux (pages [6, 11])
- System answer: Section: 3.3 LightingController
LightingController controls the low beam, high beam, daytime running lights (DRL) and the turn
indicators. Its runnable executes every 50 ms.
Automatic headlights: the low beam is switched on when the ambient light is below 400 lux for 5
seconds, and switched off when it is above 800 lux for 5 seconds. The gap between 400 and 800 lux
is a hysteresis.
The turn indicator flash frequency is 1.5 Hz (90 flashes per minute). Hazard lights override the turn
indicators.
Bulb failure is detected by current monitoring. When a bulb failure is detected, the indicator flash rate
doubles to 3 Hz to warn the driver. [Page 6]
- Cited pages: [6] | Retrieved pages: [6, 11, 14, 13] | Top distance: 0.277 | Mode: extractive
- Correct: True

### Q12. What is the turn indicator flash frequency?
- Expected: 1.5 Hz (pages [6])
- System answer: Section: 3.3 LightingController
LightingController controls the low beam, high beam, daytime running lights (DRL) and the turn
indicators. Its runnable executes every 50 ms.
Automatic headlights: the low beam is switched on when the ambient light is below 400 lux for 5
seconds, and switched off when it is above 800 lux for 5 seconds. The gap between 400 and 800 lux
is a hysteresis.
The turn indicator flash frequency is 1.5 Hz (90 flashes per minute). Hazard lights override the turn
indicators.
Bulb failure is detected by current monitoring. When a bulb failure is detected, the indicator flash rate
doubles to 3 Hz to warn the driver. [Page 6]
- Cited pages: [6] | Retrieved pages: [6, 9, 11, 14] | Top distance: 0.233 | Mode: extractive
- Correct: True

### Q13. What happens to the indicator flash rate when a bulb fails?
- Expected: It doubles to 3 Hz (pages [6])
- System answer: Section: 3.3 LightingController
LightingController controls the low beam, high beam, daytime running lights (DRL) and the turn
indicators. Its runnable executes every 50 ms.
Automatic headlights: the low beam is switched on when the ambient light is below 400 lux for 5
seconds, and switched off when it is above 800 lux for 5 seconds. The gap between 400 and 800 lux
is a hysteresis.
The turn indicator flash frequency is 1.5 Hz (90 flashes per minute). Hazard lights override the turn
indicators.
Bulb failure is detected by current monitoring. When a bulb failure is detected, the indicator flash rate
doubles to 3 Hz to warn the driver. [Page 6]
- Cited pages: [6] | Retrieved pages: [6, 13, 11, 14] | Top distance: 0.313 | Mode: extractive
- Correct: True

### Q14. What are the BCM power modes?
- Expected: SLEEP, STANDBY and RUN (pages [7])
- System answer: Section: 3.4 PowerModeManager and BcmDiagnostics
PowerModeManager controls the ECU power state. There are three BCM power modes: SLEEP,
STANDBY and RUN.
Wake-up sources are a CAN wake-up, a door switch and the ignition signal.
After ignition off, the BCM stays in RUN for 30 seconds and then moves to STANDBY. After 10
minutes without activity, STANDBY moves to SLEEP. In SLEEP the current draw must stay below
100 microamps.
BcmDiagnostics implements UDS over CAN and reports faults to the Diagnostic Event Manager
(Dem). It runs every 100 ms. [Page 7]
- Cited pages: [7] | Retrieved pages: [7, 2, 8, 3] | Top distance: 0.184 | Mode: extractive
- Correct: True

### Q15. How long does the BCM stay in RUN after ignition off?
- Expected: 30 seconds (pages [7])
- System answer: Section: 3.4 PowerModeManager and BcmDiagnostics
PowerModeManager controls the ECU power state. There are three BCM power modes: SLEEP,
STANDBY and RUN.
Wake-up sources are a CAN wake-up, a door switch and the ignition signal.
After ignition off, the BCM stays in RUN for 30 seconds and then moves to STANDBY. After 10
minutes without activity, STANDBY moves to SLEEP. In SLEEP the current draw must stay below
100 microamps.
BcmDiagnostics implements UDS over CAN and reports faults to the Diagnostic Event Manager
(Dem). It runs every 100 ms. [Page 7]
- Cited pages: [7] | Retrieved pages: [7, 10, 2, 13] | Top distance: 0.229 | Mode: extractive
- Correct: True

### Q16. What interface type is the port Pp_BcmMode?
- Expected: Mode-Switch (pages [8])
- System answer: Section: 4. Interfaces and Ports
The table lists the main ports of the BCM software components.
Port name Interface type Provider Consumer
Pp_LockState Sender-Receiver DoorLockManager BcmDiagnostics
Rp_VehicleSpeed Sender-Receiver Com (CAN) DoorLockManager
Rp_CrashDetected Sender-Receiver Com (CAN) DoorLockManager
Pp_WindowPosition Sender-Receiver WindowControl BcmDiagnostics
Rp_BatteryVoltage Sender-Receiver IoHwAb (ADC) WindowControl
Rp_AmbientLux Sender-Receiver IoHwAb (ADC) LightingController
Pp_BcmMode Mode-Switch PowerModeManager All other SWCs
Cs_NvmWrite Client-Server NvM DoorLockManager [Page 8]
- Cited pages: [8] | Retrieved pages: [8, 3, 1, 12] | Top distance: 0.196 | Mode: extractive
- Correct: True

### Q17. Which component consumes the port Rp_AmbientLux?
- Expected: LightingController (pages [8])
- System answer: Not found in the document.
- Cited pages: [] | Retrieved pages: [8, 12, 3, 11] | Top distance: 0.343 | Mode: threshold-refusal
- Correct: False

### Q18. What is the CAN ID of the ACU_Crash message?
- Expected: 0x0C5 (pages [9])
- System answer: Not found in the document.
- Cited pages: [] | Retrieved pages: [9, 13, 8, 14] | Top distance: 0.348 | Mode: threshold-refusal
- Correct: False

### Q19. What is the cycle time of the DoorLockStatus signal?
- Expected: 100 ms (pages [9])
- System answer: Section: 6. Functional Flow: Central Locking
The central-locking flow has six steps:
1. A lock request arrives over CAN in the signal LockRequest.
2. PowerModeManager moves the BCM to RUN mode if it is not already in RUN.
3. DoorLockManager checks that all doors are closed using the door switches.
4. If any door is open, the lock request is rejected and a warning chime is requested.
5. Otherwise the lock actuators are driven with a pulse of 400 ms.
6. DoorLockStatus is updated on CAN and the new state is written to NvM. [Page 10]
- Cited pages: [10] | Retrieved pages: [10, 4, 9, 12] | Top distance: 0.267 | Mode: extractive
- Correct: False

### Q20. How long is the lock actuator pulse in the central-locking flow?
- Expected: 400 ms (pages [10, 13])
- System answer: Section: 6. Functional Flow: Central Locking
The central-locking flow has six steps:
1. A lock request arrives over CAN in the signal LockRequest.
2. PowerModeManager moves the BCM to RUN mode if it is not already in RUN.
3. DoorLockManager checks that all doors are closed using the door switches.
4. If any door is open, the lock request is rejected and a warning chime is requested.
5. Otherwise the lock actuators are driven with a pulse of 400 ms.
6. DoorLockStatus is updated on CAN and the new state is written to NvM. [Page 10]
- Cited pages: [10] | Retrieved pages: [10, 13, 4, 7] | Top distance: 0.247 | Mode: extractive
- Correct: True

### Q21. What happens in central locking if a door is open?
- Expected: Lock request is rejected and a warning chime is requested (pages [10])
- System answer: Section: 6. Functional Flow: Central Locking
The central-locking flow has six steps:
1. A lock request arrives over CAN in the signal LockRequest.
2. PowerModeManager moves the BCM to RUN mode if it is not already in RUN.
3. DoorLockManager checks that all doors are closed using the door switches.
4. If any door is open, the lock request is rejected and a warning chime is requested.
5. Otherwise the lock actuators are driven with a pulse of 400 ms.
6. DoorLockStatus is updated on CAN and the new state is written to NvM. [Page 10]
- Cited pages: [10] | Retrieved pages: [10, 4, 13, 5] | Top distance: 0.242 | Mode: extractive
- Correct: True

### Q22. What does the BCM do if the ambient light sensor is faulty?
- Expected: Low beam is switched on by default (pages [11])
- System answer: Section: 9. Diagnostics and Error Handling
The BCM supports these UDS services: 0x10 DiagnosticSessionControl, 0x22 ReadDataByIdentifier,
0x19 ReadDTCInformation and 0x14 ClearDiagnosticInformation.
DTC Description Trigger
0xB10001 Door lock actuator open circuit No actuator current during the 400 ms lock pulse
0xB10002 Window anti-pinch triggered Anti-pinch reversal detected
0xB20001 Headlamp bulb failure Bulb current below the expected range
0xC10001 Lost communication with ESC No ESC_Status message received for 100 ms
Fault reaction: if VehicleSpeed is missing (DTC 0xC10001), the auto-lock function is disabled. [Page 13]
- Cited pages: [13] | Retrieved pages: [13, 2, 7, 1] | Top distance: 0.283 | Mode: extractive
- Correct: False

### Q23. Which BSW modules does BcmDiagnostics depend on?
- Expected: Dcm, Dem, Com (pages [12])
- System answer: Section: 8. Dependencies and BSW Configuration
The table shows which Basic Software modules each software component depends on.
Software component Depends on BSW modules
DoorLockManager Com, NvM, Dio
WindowControl Com, LinIf, Adc (via IoHwAb)
LightingController Pwm, Adc, Com
PowerModeManager EcuM, BswM, ComM
BcmDiagnostics Dcm, Dem, Com
The operating system has four cyclic tasks: Task_10ms (highest priority), Task_20ms, Task_50ms
and Task_100ms (lowest priority).
The NvM block NvM_DoorLockState has a size of 4 bytes. Estimated flash usage is 1.2 MB of 2 MB,
and estimated RAM usage is 70 KB of 128 KB. [Page 12]
- Cited pages: [12] | Retrieved pages: [12, 1, 8, 7] | Top distance: 0.311 | Mode: extractive
- Correct: True

### Q24. How many cyclic OS tasks does the BCM have?
- Expected: Four (pages [12])
- System answer: Section: 8. Dependencies and BSW Configuration
The table shows which Basic Software modules each software component depends on.
Software component Depends on BSW modules
DoorLockManager Com, NvM, Dio
WindowControl Com, LinIf, Adc (via IoHwAb)
LightingController Pwm, Adc, Com
PowerModeManager EcuM, BswM, ComM
BcmDiagnostics Dcm, Dem, Com
The operating system has four cyclic tasks: Task_10ms (highest priority), Task_20ms, Task_50ms
and Task_100ms (lowest priority).
The NvM block NvM_DoorLockState has a size of 4 bytes. Estimated flash usage is 1.2 MB of 2 MB,
and estimated RAM usage is 70 KB of 128 KB. [Page 12]
- Cited pages: [12] | Retrieved pages: [12, 2, 3, 1] | Top distance: 0.234 | Mode: extractive
- Correct: True

### Q25. Which DTC is set when communication with the ESC is lost?
- Expected: 0xC10001 (pages [13])
- System answer: Section: 9. Diagnostics and Error Handling
The BCM supports these UDS services: 0x10 DiagnosticSessionControl, 0x22 ReadDataByIdentifier,
0x19 ReadDTCInformation and 0x14 ClearDiagnosticInformation.
DTC Description Trigger
0xB10001 Door lock actuator open circuit No actuator current during the 400 ms lock pulse
0xB10002 Window anti-pinch triggered Anti-pinch reversal detected
0xB20001 Headlamp bulb failure Bulb current below the expected range
0xC10001 Lost communication with ESC No ESC_Status message received for 100 ms
Fault reaction: if VehicleSpeed is missing (DTC 0xC10001), the auto-lock function is disabled. [Page 13]
- Cited pages: [13] | Retrieved pages: [13, 9, 7, 3] | Top distance: 0.33 | Mode: extractive
- Correct: True

### Q26. Which UDS service reads DTC information?
- Expected: 0x19 ReadDTCInformation (pages [13])
- System answer: Section: 9. Diagnostics and Error Handling
The BCM supports these UDS services: 0x10 DiagnosticSessionControl, 0x22 ReadDataByIdentifier,
0x19 ReadDTCInformation and 0x14 ClearDiagnosticInformation.
DTC Description Trigger
0xB10001 Door lock actuator open circuit No actuator current during the 400 ms lock pulse
0xB10002 Window anti-pinch triggered Anti-pinch reversal detected
0xB20001 Headlamp bulb failure Bulb current below the expected range
0xC10001 Lost communication with ESC No ESC_Status message received for 100 ms
Fault reaction: if VehicleSpeed is missing (DTC 0xC10001), the auto-lock function is disabled. [Page 13]
- Cited pages: [13] | Retrieved pages: [13, 8, 3, 9] | Top distance: 0.29 | Mode: extractive
- Correct: True

### Q27. What is open issue OI-01?
- Expected: Confirm the anti-pinch force threshold with the supplier (pages [14])
- System answer: Section: 10. Revision History and Open Issues
Version Date Author Change
0.1 2026-07-01 Architecture Team Initial draft
0.5 2026-08-10 Architecture Team Added window and lighting components
1.0 2026-09-15 Architecture Team Approved baseline
Open issues:
OI-01: Confirm the anti-pinch force threshold with the supplier (owner: Body Team B).
OI-02: Decide whether remote window close should be supported.
OI-03: Define the method to measure the SLEEP current. [Page 14]
- Cited pages: [14] | Retrieved pages: [14, 13, 1, 8] | Top distance: 0.322 | Mode: extractive
- Correct: True

### Q28. What is the date of the approved version 1.0?
- Expected: 2026-09-15 (pages [1, 14])
- System answer: Not found in the document.
- Cited pages: [] | Retrieved pages: [14, 1, 13, 10] | Top distance: 0.353 | Mode: threshold-refusal
- Correct: False

### Q29. What is the current limit of the wiper motor?
- Expected: Not in document (wipers are out of scope) (pages [])
- System answer: Not found in the document.
- Cited pages: [] | Retrieved pages: [5, 9, 14, 7] | Top distance: 0.35 | Mode: threshold-refusal
- Correct: True

### Q30. Which Ethernet switch chip does the BCM use?
- Expected: Not in document (pages [])
- System answer: Not found in the document.
- Cited pages: [] | Retrieved pages: [8, 2, 7, 3] | Top distance: 0.341 | Mode: threshold-refusal
- Correct: True
