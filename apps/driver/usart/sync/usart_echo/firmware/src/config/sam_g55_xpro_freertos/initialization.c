/*******************************************************************************
  System Initialization File

  File Name:
    initialization.c

  Summary:
    This file contains source code necessary to initialize the system.

  Description:
    This file contains source code necessary to initialize the system.  It
    implements the "SYS_Initialize" function, defines the configuration bits,
    and allocates any necessary global system resources,
 *******************************************************************************/

// DOM-IGNORE-BEGIN
/*******************************************************************************
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
 *******************************************************************************/
// DOM-IGNORE-END

// *****************************************************************************
// *****************************************************************************
// Section: Included Files
// *****************************************************************************
// *****************************************************************************
#include "configuration.h"
#include "definitions.h"
#include "device.h"



// ****************************************************************************
// ****************************************************************************
// Section: Configuration Bits
// ****************************************************************************
// ****************************************************************************
#pragma config SECURITY_BIT = CLEAR
#pragma config BOOT_MODE = SET




// *****************************************************************************
// *****************************************************************************
// Section: Driver Initialization Data
// *****************************************************************************
// *****************************************************************************
// <editor-fold defaultstate="collapsed" desc="DRV_USART Instance 0 Initialization Data">

static DRV_USART_CLIENT_OBJ drvUSART0ClientObjPool[DRV_USART_CLIENTS_NUMBER_IDX0];


const DRV_USART_PLIB_INTERFACE drvUsart0PlibAPI = {
    .readCallbackRegister = (DRV_USART_PLIB_READ_CALLBACK_REG)FLEXCOM7_USART_ReadCallbackRegister,
    .read = (DRV_USART_PLIB_READ)FLEXCOM7_USART_Read,
    .readIsBusy = (DRV_USART_PLIB_READ_IS_BUSY)FLEXCOM7_USART_ReadIsBusy,
    .readCountGet = (DRV_USART_PLIB_READ_COUNT_GET)FLEXCOM7_USART_ReadCountGet,
    .writeCallbackRegister = (DRV_USART_PLIB_WRITE_CALLBACK_REG)FLEXCOM7_USART_WriteCallbackRegister,
    .write = (DRV_USART_PLIB_WRITE)FLEXCOM7_USART_Write,
    .writeIsBusy = (DRV_USART_PLIB_WRITE_IS_BUSY)FLEXCOM7_USART_WriteIsBusy,
    .writeCountGet = (DRV_USART_PLIB_WRITE_COUNT_GET)FLEXCOM7_USART_WriteCountGet,
    .errorGet = (DRV_USART_PLIB_ERROR_GET)FLEXCOM7_USART_ErrorGet,
    .serialSetup = (DRV_USART_PLIB_SERIAL_SETUP)FLEXCOM7_USART_SerialSetup
};

const uint32_t drvUsart0remapDataWidth[] = { 0x0, 0x40, 0x80, 0xC0, 0x20000 };
const uint32_t drvUsart0remapParity[] = { 0x800, 0x0, 0x200, 0x600, 0x400, 0xC00 };
const uint32_t drvUsart0remapStopBits[] = { 0x0, 0x1000, 0x2000 };
const uint32_t drvUsart0remapError[] = { 0x20, 0x80, 0x40 };

const DRV_USART_INIT drvUsart0InitData =
{
    .usartPlib = &drvUsart0PlibAPI,

    /* USART Number of clients */
    .numClients = DRV_USART_CLIENTS_NUMBER_IDX0,

    /* USART Client Objects Pool */
    .clientObjPool = (uintptr_t)&drvUSART0ClientObjPool[0],


    .remapDataWidth = drvUsart0remapDataWidth,

    .remapParity = drvUsart0remapParity,

    .remapStopBits = drvUsart0remapStopBits,

    .remapError = drvUsart0remapError,
};

// </editor-fold>


// *****************************************************************************
// *****************************************************************************
// Section: System Data
// *****************************************************************************
// *****************************************************************************
/* Structure to hold the object handles for the modules in the system. */
SYSTEM_OBJECTS sysObj;

// *****************************************************************************
// *****************************************************************************
// Section: Library/Stack Initialization Data
// *****************************************************************************
// *****************************************************************************


// *****************************************************************************
// *****************************************************************************
// Section: System Initialization
// *****************************************************************************
// *****************************************************************************



/*******************************************************************************
  Function:
    void SYS_Initialize ( void *data )

  Summary:
    Initializes the board, services, drivers, application and other modules.

  Remarks:
 */

void SYS_Initialize ( void* data )
{

    EFC_Initialize();
  
	PIO_Initialize();

    CLOCK_Initialize();



	BSP_Initialize();
    FLEXCOM7_USART_Initialize();

	WDT_REGS->WDT_MR = WDT_MR_WDDIS_Msk; 		// Disable WDT 


    sysObj.drvUsart0 = DRV_USART_Initialize(DRV_USART_INDEX_0, (SYS_MODULE_INIT *)&drvUsart0InitData);




    APP_USART_ECHO_Initialize();


    NVIC_Initialize();

}


/*******************************************************************************
 End of File
*/
