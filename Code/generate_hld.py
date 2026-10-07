"""Creates the SYNTHETIC AUTOSAR-style HLD (PDF) and the ground-truth test questions.

All content is invented for academic use. No real company data.
Run:  python Code/generate_hld.py
Output: Input_Data/BCM_HLD_v1.0.pdf and Input_Data/test_questions.json
"""
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent.parent
PDF_OUT = ROOT / "Input_Data" / "BCM_HLD_v1.0.pdf"
Q_OUT = ROOT / "Input_Data" / "test_questions.json"

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=16, spaceAfter=8)
BODY = ParagraphStyle("B", parent=ss["Normal"], fontSize=10.5, leading=15, spaceAfter=6)
CELL = ParagraphStyle("C", parent=ss["Normal"], fontSize=9, leading=11)
CELLH = ParagraphStyle("CH", parent=CELL, textColor=colors.white, fontName="Helvetica-Bold")


def table(rows, widths):
    data = [[Paragraph(c, CELLH) for c in rows[0]]]
    data += [[Paragraph(c, CELL) for c in r] for r in rows[1:]]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3A5F")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F7")]),
    ]))
    return t


# Each entry = one PDF page: (heading, [paragraph strings], optional table (rows, widths), [paragraphs after table])
PAGES = [
    ("Body Control Module (BCM) - High-Level Design", [
        "Document ID: HLD-BCM-001. Version: 1.0. Date: 2026-09-15. Status: Approved baseline.",
        "Author: Architecture Team. Project: NovaDrive BCM (fictional).",
        "This is a SYNTHETIC document created for academic evaluation of a RAG assistant. "
        "It contains no real company or customer data.",
    ], None, []),

    ("1. Introduction and Scope", [
        "This document describes the high-level design of the Body Control Module (BCM). "
        "The BCM controls the central door locks, the power windows and the exterior lighting of the vehicle.",
        "The BCM software is built on the AUTOSAR Classic Platform, release R21-11. "
        "The application layer contains five software components: DoorLockManager, WindowControl, "
        "LightingController, PowerModeManager and BcmDiagnostics.",
        "Out of scope for this release: wipers, climate control (HVAC) and passive keyless entry.",
    ], None, []),

    ("2. Architecture Overview", [
        "The software is organised in layers: the application layer with five software components, the Runtime "
        "Environment (RTE), the Basic Software (BSW) services (Com, NvM, Dem, Dcm), the ECU abstraction layer and "
        "the microcontroller abstraction layer (MCAL).",
        "The BCM is connected to the body CAN bus at 500 kbit/s. The window switches are connected over LIN at 19.2 kbit/s.",
    ], ([["Component", "Type", "Runnable period", "Owner team"],
         ["DoorLockManager", "Application SWC", "10 ms", "Body Team A"],
         ["WindowControl", "Application SWC", "20 ms", "Body Team B"],
         ["LightingController", "Application SWC", "50 ms", "Lighting Team"],
         ["PowerModeManager", "Service SWC", "10 ms", "Platform Team"],
         ["BcmDiagnostics", "Application SWC", "100 ms", "Diagnostics Team"]],
        [45, 40, 35, 45]), []),

    ("3.1 DoorLockManager", [
        "DoorLockManager locks and unlocks the four doors. It handles central-locking requests, automatic locking "
        "while driving and crash unlock.",
        "Its runnable DoorLock_Run10ms executes every 10 ms. The lock actuators are driven through a Dio channel group.",
        "Crash unlock: when the signal CrashDetected is set to 1 by the airbag control unit, DoorLockManager unlocks "
        "all doors within 100 ms.",
        "Auto-lock: when VehicleSpeed is above 10 km/h, all doors are locked automatically.",
        "The last lock state is stored in the NvM block NvM_DoorLockState so it survives a power cycle.",
    ], None, []),

    ("3.2 WindowControl", [
        "WindowControl drives the four window motors. It supports manual up/down and one-touch up/down. "
        "Its runnable executes every 20 ms.",
        "Anti-pinch: during one-touch close, an obstruction is detected from the motor current. On detection the "
        "motor is reversed for 200 ms.",
        "The maximum one-touch travel time is 4 seconds.",
        "Window operation is disabled when the battery voltage is below 9 V, to protect the battery.",
        "The window switch inputs arrive over LIN from the door switch pods.",
    ], None, []),

    ("3.3 LightingController", [
        "LightingController controls the low beam, high beam, daytime running lights (DRL) and the turn indicators. "
        "Its runnable executes every 50 ms.",
        "Automatic headlights: the low beam is switched on when the ambient light is below 400 lux for 5 seconds, and "
        "switched off when it is above 800 lux for 5 seconds. The gap between 400 and 800 lux is a hysteresis.",
        "The turn indicator flash frequency is 1.5 Hz (90 flashes per minute). Hazard lights override the turn indicators.",
        "Bulb failure is detected by current monitoring. When a bulb failure is detected, the indicator flash rate "
        "doubles to 3 Hz to warn the driver.",
    ], None, []),

    ("3.4 PowerModeManager and BcmDiagnostics", [
        "PowerModeManager controls the ECU power state. There are three BCM power modes: SLEEP, STANDBY and RUN.",
        "Wake-up sources are a CAN wake-up, a door switch and the ignition signal.",
        "After ignition off, the BCM stays in RUN for 30 seconds and then moves to STANDBY. After 10 minutes without "
        "activity, STANDBY moves to SLEEP. In SLEEP the current draw must stay below 100 microamps.",
        "BcmDiagnostics implements UDS over CAN and reports faults to the Diagnostic Event Manager (Dem). "
        "It runs every 100 ms.",
    ], None, []),

    ("4. Interfaces and Ports", [
        "The table lists the main ports of the BCM software components.",
    ], ([["Port name", "Interface type", "Provider", "Consumer"],
         ["Pp_LockState", "Sender-Receiver", "DoorLockManager", "BcmDiagnostics"],
         ["Rp_VehicleSpeed", "Sender-Receiver", "Com (CAN)", "DoorLockManager"],
         ["Rp_CrashDetected", "Sender-Receiver", "Com (CAN)", "DoorLockManager"],
         ["Pp_WindowPosition", "Sender-Receiver", "WindowControl", "BcmDiagnostics"],
         ["Rp_BatteryVoltage", "Sender-Receiver", "IoHwAb (ADC)", "WindowControl"],
         ["Rp_AmbientLux", "Sender-Receiver", "IoHwAb (ADC)", "LightingController"],
         ["Pp_BcmMode", "Mode-Switch", "PowerModeManager", "All other SWCs"],
         ["Cs_NvmWrite", "Client-Server", "NvM", "DoorLockManager"]],
        [38, 35, 42, 40]), []),

    ("5. CAN Signals and Messages", [
        "All messages below are on the body CAN bus at 500 kbit/s.",
    ], ([["Signal", "Message", "CAN ID", "Direction", "Cycle"],
         ["VehicleSpeed", "ESC_Status", "0x1A0", "Rx", "20 ms"],
         ["CrashDetected", "ACU_Crash", "0x0C5", "Rx", "Event-triggered"],
         ["IgnitionState", "IGN_Status", "0x120", "Rx", "50 ms"],
         ["DoorLockStatus", "BCM_Body1", "0x3B0", "Tx", "100 ms"],
         ["WindowPos_FL", "BCM_Window", "0x3B8", "Tx", "100 ms"],
         ["HeadlampState", "BCM_Light", "0x3C0", "Tx", "200 ms"]],
        [32, 32, 25, 25, 36]), []),

    ("6. Functional Flow: Central Locking", [
        "The central-locking flow has six steps:",
        "1. A lock request arrives over CAN in the signal LockRequest.",
        "2. PowerModeManager moves the BCM to RUN mode if it is not already in RUN.",
        "3. DoorLockManager checks that all doors are closed using the door switches.",
        "4. If any door is open, the lock request is rejected and a warning chime is requested.",
        "5. Otherwise the lock actuators are driven with a pulse of 400 ms.",
        "6. DoorLockStatus is updated on CAN and the new state is written to NvM.",
    ], None, []),

    ("7. Functional Flow: Automatic Headlights", [
        "The automatic headlight flow works as follows:",
        "1. The ambient light value (Rp_AmbientLux) is read every 50 ms.",
        "2. The value is filtered with a moving average over 8 samples.",
        "3. If the filtered value stays below 400 lux for 5 seconds, the low beam is switched on.",
        "4. If the filtered value stays above 800 lux for 5 seconds, the low beam is switched off.",
        "5. A manual switch position always overrides the automatic function.",
        "Fail-safe: if the light sensor is faulty, the low beam is switched on by default.",
    ], None, []),

    ("8. Dependencies and BSW Configuration", [
        "The table shows which Basic Software modules each software component depends on.",
    ], ([["Software component", "Depends on BSW modules"],
         ["DoorLockManager", "Com, NvM, Dio"],
         ["WindowControl", "Com, LinIf, Adc (via IoHwAb)"],
         ["LightingController", "Pwm, Adc, Com"],
         ["PowerModeManager", "EcuM, BswM, ComM"],
         ["BcmDiagnostics", "Dcm, Dem, Com"]],
        [60, 100]),
     ["The operating system has four cyclic tasks: Task_10ms (highest priority), Task_20ms, Task_50ms and Task_100ms (lowest priority).",
      "The NvM block NvM_DoorLockState has a size of 4 bytes. Estimated flash usage is 1.2 MB of 2 MB, "
      "and estimated RAM usage is 70 KB of 128 KB."]),

    ("9. Diagnostics and Error Handling", [
        "The BCM supports these UDS services: 0x10 DiagnosticSessionControl, 0x22 ReadDataByIdentifier, "
        "0x19 ReadDTCInformation and 0x14 ClearDiagnosticInformation.",
    ], ([["DTC", "Description", "Trigger"],
         ["0xB10001", "Door lock actuator open circuit", "No actuator current during the 400 ms lock pulse"],
         ["0xB10002", "Window anti-pinch triggered", "Anti-pinch reversal detected"],
         ["0xB20001", "Headlamp bulb failure", "Bulb current below the expected range"],
         ["0xC10001", "Lost communication with ESC", "No ESC_Status message received for 100 ms"]],
        [25, 60, 75]),
     ["Fault reaction: if VehicleSpeed is missing (DTC 0xC10001), the auto-lock function is disabled."]),

    ("10. Revision History and Open Issues", [], ([
        ["Version", "Date", "Author", "Change"],
        ["0.1", "2026-07-01", "Architecture Team", "Initial draft"],
        ["0.5", "2026-08-10", "Architecture Team", "Added window and lighting components"],
        ["1.0", "2026-09-15", "Architecture Team", "Approved baseline"]],
        [20, 30, 45, 65]),
     ["Open issues:",
      "OI-01: Confirm the anti-pinch force threshold with the supplier (owner: Body Team B).",
      "OI-02: Decide whether remote window close should be supported.",
      "OI-03: Define the method to measure the SLEEP current."]),
]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawString(20 * mm, 10 * mm, f"HLD-BCM-001 v1.0 | Synthetic document | Page {doc.page}")
    canvas.restoreState()


def build_pdf():
    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(PDF_OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=18 * mm, title="BCM High-Level Design (Synthetic)")
    story = []
    for i, (title, paras, tbl, after) in enumerate(PAGES):
        story.append(Paragraph(title, H1))
        for p in paras:
            story.append(Paragraph(p, BODY))
        if tbl:
            story += [Spacer(1, 4), table(*tbl), Spacer(1, 8)]
        for p in after:
            story.append(Paragraph(p, BODY))
        if i < len(PAGES) - 1:
            story.append(PageBreak())
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def Q(i, q, ans, must, pages, answerable=True):
    return {"id": i, "question": q, "expected_answer": ans, "must_include": must,
            "pages": pages, "answerable": answerable}


QUESTIONS = [
    Q(1, "Which AUTOSAR platform and release does the BCM use?", "AUTOSAR Classic Platform R21-11", [["classic"], ["r21-11"]], [2]),
    Q(2, "How many software components are in the application layer?", "Five", [["five", "5"]], [2, 3]),
    Q(3, "What is the runnable period of DoorLockManager?", "10 ms", [["10 ms"]], [3, 4]),
    Q(4, "Which team owns LightingController?", "Lighting Team", [["lighting team"]], [3]),
    Q(5, "What bit rate does the body CAN bus use?", "500 kbit/s", [["500"]], [3, 9]),
    Q(6, "What does DoorLockManager do when CrashDetected is set?", "Unlocks all doors within 100 ms", [["unlock"], ["100 ms"]], [4]),
    Q(7, "At what vehicle speed are the doors locked automatically?", "Above 10 km/h", [["10 km/h"]], [4]),
    Q(8, "Which NvM block stores the door lock state?", "NvM_DoorLockState", [["nvm_doorlockstate"]], [4, 12]),
    Q(9, "How long does the window motor reverse after anti-pinch detection?", "200 ms", [["200 ms"]], [5]),
    Q(10, "Below which battery voltage is window operation disabled?", "9 V", [["9 v"]], [5]),
    Q(11, "What are the lux thresholds for automatic headlights?", "On below 400 lux, off above 800 lux", [["400"], ["800"]], [6, 11]),
    Q(12, "What is the turn indicator flash frequency?", "1.5 Hz", [["1.5 hz"]], [6]),
    Q(13, "What happens to the indicator flash rate when a bulb fails?", "It doubles to 3 Hz", [["3 hz", "doubles"]], [6]),
    Q(14, "What are the BCM power modes?", "SLEEP, STANDBY and RUN", [["sleep"], ["standby"], ["run"]], [7]),
    Q(15, "How long does the BCM stay in RUN after ignition off?", "30 seconds", [["30 s"]], [7]),
    Q(16, "What interface type is the port Pp_BcmMode?", "Mode-Switch", [["mode-switch", "mode switch"]], [8]),
    Q(17, "Which component consumes the port Rp_AmbientLux?", "LightingController", [["lightingcontroller"]], [8]),
    Q(18, "What is the CAN ID of the ACU_Crash message?", "0x0C5", [["0x0c5"]], [9]),
    Q(19, "What is the cycle time of the DoorLockStatus signal?", "100 ms", [["100 ms"]], [9]),
    Q(20, "How long is the lock actuator pulse in the central-locking flow?", "400 ms", [["400 ms"]], [10, 13]),
    Q(21, "What happens in central locking if a door is open?", "Lock request is rejected and a warning chime is requested", [["reject", "not be locked", "refus"]], [10]),
    Q(22, "What does the BCM do if the ambient light sensor is faulty?", "Low beam is switched on by default", [["low beam"]], [11]),
    Q(23, "Which BSW modules does BcmDiagnostics depend on?", "Dcm, Dem, Com", [["dcm"], ["dem"], ["com"]], [12]),
    Q(24, "How many cyclic OS tasks does the BCM have?", "Four", [["four", "4"]], [12]),
    Q(25, "Which DTC is set when communication with the ESC is lost?", "0xC10001", [["0xc10001"]], [13]),
    Q(26, "Which UDS service reads DTC information?", "0x19 ReadDTCInformation", [["0x19"]], [13]),
    Q(27, "What is open issue OI-01?", "Confirm the anti-pinch force threshold with the supplier", [["anti-pinch"], ["threshold"]], [14]),
    Q(28, "What is the date of the approved version 1.0?", "2026-09-15", [["2026-09-15"]], [1, 14]),
    # Not in the document: the system must refuse
    Q(29, "What is the current limit of the wiper motor?", "Not in document (wipers are out of scope)", [], [], False),
    Q(30, "Which Ethernet switch chip does the BCM use?", "Not in document", [], [], False),
]

if __name__ == "__main__":
    build_pdf()
    Q_OUT.write_text(json.dumps(QUESTIONS, indent=2), encoding="utf-8")
    print(f"Wrote {PDF_OUT}")
    print(f"Wrote {Q_OUT} ({len(QUESTIONS)} questions)")
