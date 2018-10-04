# coding: utf-8
"""*****************************************************************************
* Copyright (C) 2018 Microchip Technology Inc. and its subsidiaries.
*
* Subject to your compliance with these terms, you may use Microchip software
* and any derivatives exclusively with Microchip products. It is your
* responsibility to comply with third party license terms applicable to your
* use of third party software (including open source software) that may
* accompany Microchip software.
*
* THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
* EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
* WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
* PARTICULAR PURPOSE.
*
* IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
* INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND
* WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS
* BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
* FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
* ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
* THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
*****************************************************************************"""

################################################################################
#### Component ####
################################################################################

at25MemoryInterruptEnable = None

def at25SetMemoryDependency(symbol, event):
    if (event["value"] == True):
        symbol.setVisible(True)
    else:
        symbol.setVisible(False)

#def updatePinPosition(symbol, event):
    # TBD: "value" of at25SymChipSelectPin and other pin symbols should be updated
    # here based on the package selected in Pin manager.


def instantiateComponent(at25Component):
    global at25MemoryInterruptEnable

    res = Database.activateComponents(["HarmonyCore"])

    # Enable "Generate Harmony Driver Common Files" option in MHC
    Database.setSymbolValue("HarmonyCore", "ENABLE_DRV_COMMON", True, 1)

    # Enable "Generate Harmony System Service Common Files" option in MHC
    Database.setSymbolValue("HarmonyCore", "ENABLE_SYS_COMMON", True, 1)

    # Enable "Enable System Ports" option in MHC
    Database.setSymbolValue("HarmonyCore", "ENABLE_SYS_PORTS", True, 1)

    at25SymNumInst = at25Component.createIntegerSymbol("DRV_AT25_NUM_INSTANCES", None)
    at25SymNumInst.setLabel("Number of Instances")
    at25SymNumInst.setDefaultValue(1)
    at25SymNumInst.setVisible(False)

    #at25SymIndex = at25Component.createIntegerSymbol("DRV_AT25_INDEX", None)
    #at25SymIndex.setLabel("Driver Index")
    #at25SymIndex.setVisible(True)
    #at25SymIndex.setDefaultValue(0)
    #at25SymIndex.setReadOnly(True)

    at25PLIB = at25Component.createStringSymbol("DRV_AT25_PLIB", None)
    at25PLIB.setLabel("PLIB Used")
    at25PLIB.setReadOnly(True)

    at25SymNumClients = at25Component.createIntegerSymbol("DRV_AT25_NUM_CLIENTS", None)
    at25SymNumClients.setLabel("Number of Clients")
    at25SymNumClients.setReadOnly(True)
    at25SymNumClients.setDefaultValue(1)
    
    at25EEPROMPageSize = at25Component.createIntegerSymbol("EEPROM_PAGE_SIZE", None)
    at25EEPROMPageSize.setLabel("EEPROM Page Size")
    at25EEPROMPageSize.setVisible(True)
    at25EEPROMPageSize.setDefaultValue(256)
    
    at25EEPROMFlashSize = at25Component.createIntegerSymbol("EEPROM_FLASH_SIZE", None)
    at25EEPROMFlashSize.setLabel("EEPROM Flash Size")
    at25EEPROMFlashSize.setVisible(True)
    at25EEPROMFlashSize.setDefaultValue(262144)

    at25MemoryDriver = at25Component.createBooleanSymbol("DRV_MEMORY_CONNECTED", None)
    at25MemoryDriver.setLabel("Memory Driver Connected")
    at25MemoryDriver.setVisible(False)
    at25MemoryDriver.setDefaultValue(False)

    at25MemoryInterruptEnable = at25Component.createBooleanSymbol("INTERRUPT_ENABLE", None)
    at25MemoryInterruptEnable.setLabel("at25 Interrupt Enable")
    at25MemoryInterruptEnable.setVisible(False)
    at25MemoryInterruptEnable.setDefaultValue(False)
    at25MemoryInterruptEnable.setReadOnly(True)

    at25MemoryEraseEnable = at25Component.createBooleanSymbol("ERASE_ENABLE", None)
    at25MemoryEraseEnable.setLabel("at25 Erase Enable")
    at25MemoryEraseEnable.setVisible(False)
    at25MemoryEraseEnable.setDefaultValue(False)

    at25SymChipSelectPin = at25Component.createKeyValueSetSymbol("DRV_AT25_CHIP_SELECT_PIN", None)
    at25SymChipSelectPin.setLabel("Chip Select Pin")
    at25SymChipSelectPin.setDefaultValue(5) #PA5
    at25SymChipSelectPin.setOutputMode("Key")
    at25SymChipSelectPin.setDisplayMode("Description")

    at25SymHoldPin = at25Component.createKeyValueSetSymbol("DRV_AT25_HOLD_PIN", None)
    at25SymHoldPin.setLabel("Hold Pin")
    at25SymHoldPin.setDefaultValue(0) #PA0
    at25SymHoldPin.setOutputMode("Key")
    at25SymHoldPin.setDisplayMode("Description")

    at25SymWriteProtectPin = at25Component.createKeyValueSetSymbol("DRV_AT25_WRITE_PROTECT_PIN", None)
    at25SymWriteProtectPin.setLabel("Write Protect Pin")
    at25SymWriteProtectPin.setDefaultValue(1) #PA1
    at25SymWriteProtectPin.setOutputMode("Key")
    at25SymWriteProtectPin.setDisplayMode("Description")

    pinOutNode = ATDF.getNode("/avr-tools-device-file/pinouts/pinout")
    pinOut = pinOutNode.getChildren()

    for pad in range(0, len(pinOut)):
        pin = pinOut[pad].getAttribute("pad")
        if (pin[0] == "P") and (pin[-1].isdigit()):
            key = "SYS_PORT_PIN_" + pin
            value = pinOut[pad].getAttribute("position")
            description = pinOut[pad].getAttribute("pad")
            at25SymChipSelectPin.addKey(key, value, description)
            at25SymHoldPin.addKey(key, value, description)
            at25SymWriteProtectPin.addKey(key, value, description)

    at25SymPinConfigComment = at25Component.createCommentSymbol("DRV_AT25_PINS_CONFIG_COMMENT", None)
    at25SymPinConfigComment.setVisible(True)
    at25SymPinConfigComment.setLabel("***Above selected pins must be configured as GPIO Output in Pin Manager***")

    at25MemoryStartAddr = at25Component.createHexSymbol("START_ADDRESS", None)
    at25MemoryStartAddr.setLabel("AT25 EEPROM Start Address")
    at25MemoryStartAddr.setVisible(True)
    at25MemoryStartAddr.setDefaultValue(0x0000000)

    ############################################################################
    #### Code Generation ####
    ############################################################################

    configName = Variables.get("__CONFIGURATION_NAME")

    at25HeaderFile = at25Component.createFileSymbol("AT25_HEADER", None)
    at25HeaderFile.setSourcePath("driver/at25/drv_at25.h")
    at25HeaderFile.setOutputName("drv_at25.h")
    at25HeaderFile.setDestPath("driver/at25/")
    at25HeaderFile.setProjectPath("config/" + configName + "/driver/at25/")
    at25HeaderFile.setType("HEADER")
    at25HeaderFile.setOverwrite(True)

    at25SymHeaderDefFile = at25Component.createFileSymbol("DRV_AT25_DEF", None)
    at25SymHeaderDefFile.setSourcePath("driver/at25/templates/drv_at25_definitions.h.ftl")
    at25SymHeaderDefFile.setOutputName("drv_at25_definitions.h")
    at25SymHeaderDefFile.setDestPath("driver/at25")
    at25SymHeaderDefFile.setProjectPath("config/" + configName + "/driver/at25/")
    at25SymHeaderDefFile.setType("HEADER")
    at25SymHeaderDefFile.setMarkup(True)
    at25SymHeaderDefFile.setOverwrite(True)

    at25SourceFile = at25Component.createFileSymbol("AT25_SOURCE", None)
    at25SourceFile.setSourcePath("driver/at25/src/drv_at25.c")
    at25SourceFile.setOutputName("drv_at25.c")
    at25SourceFile.setDestPath("driver/at25/src")
    at25SourceFile.setProjectPath("config/" + configName + "/driver/at25/")
    at25SourceFile.setType("SOURCE")
    at25SourceFile.setOverwrite(True)
    at25SourceFile.setMarkup(False)

    at25AsyncSymHeaderLocalFile = at25Component.createFileSymbol("DRV_AT25_HEADER_LOCAL", None)
    at25AsyncSymHeaderLocalFile.setSourcePath("driver/at25/src/drv_at25_local.h")
    at25AsyncSymHeaderLocalFile.setOutputName("drv_at25_local.h")
    at25AsyncSymHeaderLocalFile.setDestPath("driver/at25/src")
    at25AsyncSymHeaderLocalFile.setProjectPath("config/" + configName + "/driver/at25/")
    at25AsyncSymHeaderLocalFile.setType("SOURCE")
    at25AsyncSymHeaderLocalFile.setOverwrite(True)
    at25AsyncSymHeaderLocalFile.setEnabled(True)


    at25SystemDefFile = at25Component.createFileSymbol("AT25_DEF", None)
    at25SystemDefFile.setType("STRING")
    at25SystemDefFile.setOutputName("core.LIST_SYSTEM_DEFINITIONS_H_INCLUDES")
    at25SystemDefFile.setSourcePath("driver/at25/templates/system/definitions.h.ftl")
    at25SystemDefFile.setMarkup(True)

    at25SymSystemDefObjFile = at25Component.createFileSymbol("DRV_AT25_SYSTEM_DEF_OBJECT", None)
    at25SymSystemDefObjFile.setType("STRING")
    at25SymSystemDefObjFile.setOutputName("core.LIST_SYSTEM_DEFINITIONS_H_OBJECTS")
    at25SymSystemDefObjFile.setSourcePath("driver/at25/templates/system/definitions_objects.h.ftl")
    at25SymSystemDefObjFile.setMarkup(True)

    at25SymSystemConfigFile = at25Component.createFileSymbol("DRV_AT25_CONFIGIRUTION", None)
    at25SymSystemConfigFile.setType("STRING")
    at25SymSystemConfigFile.setOutputName("core.LIST_SYSTEM_CONFIG_H_DRIVER_CONFIGURATION")
    at25SymSystemConfigFile.setSourcePath("driver/at25/templates/system/configuration.h.ftl")
    at25SymSystemConfigFile.setMarkup(True)

    at25SymSystemInitDataFile = at25Component.createFileSymbol("DRV_AT25_INIT_DATA", None)
    at25SymSystemInitDataFile.setType("STRING")
    at25SymSystemInitDataFile.setOutputName("core.LIST_SYSTEM_INIT_C_DRIVER_INITIALIZATION_DATA")
    at25SymSystemInitDataFile.setSourcePath("driver/at25/templates/system/initialize_data.c.ftl")
    at25SymSystemInitDataFile.setMarkup(True)

    at25SystemInitFile = at25Component.createFileSymbol("AT25_INIT", None)
    at25SystemInitFile.setType("STRING")
    at25SystemInitFile.setOutputName("core.LIST_SYSTEM_INIT_C_SYS_INITIALIZE_DRIVERS")
    at25SystemInitFile.setSourcePath("driver/at25/templates/system/initialize.c.ftl")
    at25SystemInitFile.setMarkup(True)

def onDependencyConnected(info):
    global at25MemoryInterruptEnable

    if info["dependencyID"] == "drv_at25_SPI_dependency" :
        plibUsed = info["localComponent"].getSymbolByID("DRV_AT25_PLIB")
        plibUsed.clearValue()
        at25PlibId = info["remoteComponent"].getID().upper()
        plibUsed.setValue(at25PlibId.upper(), 1)
        Database.setSymbolValue(at25PlibId, "SPI_DRIVER_CONTROLLED", True, 1)

        at25MemoryInterruptEnable.setValue(Database.getSymbolValue("core", at25PlibId + "_INTERRUPT_ENABLE"), 1)

def onDependencyDisconnected(info):
    global at25MemoryInterruptEnable

    if info["dependencyID"] == "drv_at25_SPI_dependency":
        at25PlibId = info["remoteComponent"].getID().upper()
        Database.setSymbolValue(at25PlibId, "SPI_DRIVER_CONTROLLED", False, 1)

        at25MemoryInterruptEnable.setValue(False, 1)
