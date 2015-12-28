# -*- coding: utf-8 -*-
import binascii
from . import vd_packs
from . import vd_dbconn


def GlobalCodes():
    global ERROR_0000
    global ERROR_1020
    global ERROR_1022
    global ERROR_1030
    global ERROR_2003
    global ERROR_3001
    global ERROR_3002
    global ERROR_3004
    global ERROR_3005
    global ERROR_3006
    global ERROR_3007
    global ERROR_4000
    global ERROR_5001
    global ERROR_5002
    global ERROR_5003
    global ERROR_5004
    global ERROR_5005
    global ERROR_5006
    global ERROR_5007
    global ERROR_6000
    global ERROR_7006

    ERROR_0000 = '0x30303030'
    ERROR_1020 = '0x31303230'
    ERROR_1022 = '0x31303232'
    ERROR_1030 = '0x31303333'
    ERROR_2003 = '0x32303033'
    ERROR_3001 = '0x33303031'
    ERROR_3002 = '0x33303032'
    ERROR_3004 = '0x33303034'
    ERROR_3005 = '0x33303035'
    ERROR_3006 = '0x33303036'
    ERROR_3007 = '0x33303037'
    ERROR_4000 = '0x34303030'
    ERROR_5001 = '0x35303031'
    ERROR_5002 = '0x35303032'
    ERROR_5003 = '0x35303033'
    ERROR_5004 = '0x35303034'
    ERROR_5005 = '0x35303035'
    ERROR_5006 = '0x35303036'
    ERROR_5007 = '0x35303037'
    ERROR_6000 = '0x36303030'
    ERROR_7006 = '0x37303036'


if __name__ == '__main__':
    GlobalCodes()


def comTerminalLogon(hex_data, server):
    print "Logon do Terminal \
    (Terminal -> Servidor) 0x01"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """
    GlobalCodes()
    start = hex_data[0:2]
    command = hex_data[2:4]
    cid = hex_data[4:8]
    tid = hex_data[8:16]
    param1 = server
    param2 = '0x0a000000'
    param3 = hex_data[40:44]+'000000000000'
    errorcode = ERROR_0000
    extradata = '0x0000'
    replay = vd_packs.comPackC01(start, command, cid, tid, param1, param2,
                                 param3, errorcode, extradata)
    return replay


def comTerminalLogoff(hex_data, server):
    print "Logoff do Terminal \
    (Terminal -> Servidor) 0x02"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """
    return None


def comTCardSerialNReading(hex_data, server):
    print "Leitura do número de Série do Cartão \
    (Terminal -> Servidor) 0x06"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comTimeSync(hex_data, server):
    print "Sincronismo de Hora \
    (Terminal -> Servidor) 0x09"
    """
    Rotina para envio de pacote de Sincronismo de Hora do Terminal
    (Terminal -> Servidor) código do comando 0x09
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """
    GlobalCodes()
    start = hex_data[0:2]
    command = hex_data[2:4]
    cid = hex_data[4:8]
    tid = hex_data[8:16]
    param1 = '0x00000000'
    param2 = '0x00000000'
    param3 = vd_packs.TIME_INFO()
    errorcode = ERROR_0000
    extradata = '0x0000'
    replay = vd_packs.comPackC01(start, command, cid, tid, param1, param2,
                                 param3, errorcode, extradata)
    return replay


def comSendingTerminalStatus(hex_data, server):
    # print "Enviando Status do Terminal \
    # (Terminal -> Servidor) 0x0a"
    """
    Rotina para envio de pacote de Solicitação de Status do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """
    GlobalCodes()
    start = hex_data[0:2]
    command = hex_data[2:4]
    cid = hex_data[4:8]
    tid = hex_data[8:16]
    param1 = '0x00000000'
    param2 = '0x00000000'
    param3 = vd_packs.TIME_INFO()
    errorcode = ERROR_0000
    extradata = '0x0000'
    replay = vd_packs.comPackC01(start, command, cid, tid, param1, param2,
                                 param3, errorcode, extradata)
    return replay


def comSendingAuthResult(hex_data, server):
    print "Enviando Resultado da Autenticação \
    (Terminal -> Servidor) 0x13"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comCheckUserDuplication(hex_data, server):
    print "Verificando duplicidade de usuário \
    (Terminal -> Servidor) 0x29"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comBringMealDataSum(hex_data, server):
    print "Buscando informação sobre refeições \
    (Terminal -> Servidor) 0x34"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comBringAntipassBackInfo(hex_data, server):
    print "Buscando informação de Antipass Back \
    (Terminal -> Servidor) 0x1a"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comBringUserAuthInfo(hex_data, server):
    print 'Buscando informação de autenticação de usuário \
    (Terminal -> Servidor) 0x1b'
    """
    Rotina para envio de pacote de autenticação do usuário
    (Terminal -> Servidor) código do comando 0x1b
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """
    GlobalCodes()
    tag = binascii.unhexlify(hex_data[64:]).decode()
    print 'Tag:', tag
    x = hex_data[8:16]
    tid = int("%s%s%s%s" % (x[6:8], x[4:6], x[2:4], x[0:2]), 16)
    print 'Terminal:', tid
    if (vd_dbconn.getAuth(tag, tid)):
        status = '0x0008000000000000'
        errorcode_hex = ERROR_0000
    else:
        status = '0x0108000000000000'
        errorcode_hex = ERROR_3004
    start = hex_data[0:2]
    command = hex_data[2:4]
    cid = hex_data[4:8]
    tid = hex_data[8:16]
    param1 = '0x00000000'
    param2 = '0x00000000'
    param3 = status
    errorcode = errorcode_hex
    extradata = '0x0800'
    data = vd_packs.TIME_INFO()
    replay = vd_packs.comPackC02(start, command, cid, tid, param1, param2,
                                 param3, errorcode, extradata, data)
    return replay


def comServerAuth(hex_data, server):
    print "Autenticação no Servidor \
    (Terminal -> Servidor) 0x1c"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comNCNOSignalAlarm(hex_data, server):
    print "Sinal de alarme NC/NO \
    (Terminal -> Servidor) 0x60"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comSettingTerminalOption(hex_data, server):
    print "Definindo Opção no Terminal \
    (Servidor -> Terminal) 0x05"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comSCardSerialNReading(hex_data, server):
    print "Leitura do número de Série do Cartão \
    (Servidor -> Terminal) 0x07"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comTerminalTimeSetting(hex_data, server):
    print "Definindo a hora do Terminal \
    (Servidor -> Terminal) 0x08"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comForceOpenTerminalLock(hex_data, server):
    print "Abertura forçada da trava associada ao terminal \
    (Servidor -> Terminal) 0x0c"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comControlTerminalPeripheralDevice(hex_data, server):
    print "Controle do dispositivo periférico do terminal \
    (Servidor -> Terminal) 0x0d"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comBringTerminalAuthRecord(hex_data, server):
    print "Buscando registro de autenticação do terminal \
    (Servidor -> Terminal) 0x16"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comBringTerminalAuditLog(hex_data, server):
    print "Buscando o log de auditoria do terminal \
    (Servidor -> Terminal) 0x17"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comUpgradeTerminalFirmware(hex_data, server):
    print "Realizando Upgrade de Firmware no Terminal \
    (Servidor -> Terminal) 0x20"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comBringTerminalFirmwareVersion(hex_data, server):
    print "Buscando a Versão do Firmware do Terminal \
    (Servidor -> Terminal) 0x21"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comTerminalUserSync(hex_data, server):
    print "Realizando o sincronismo dos usuários no Terminal \
    (Servidor -> Terminal) 0x27"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comSettingTerminalMealOption(hex_data, server):
    print "Definindo as opções de refeição no terminal \
    (Servidor -> Terminal) 0x33"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comShinsegyeTerminalMealUserManagement(hex_data, server):
    print "Gerenciamento das refeições dos usuários no terminal,Shinsegye \
    (Servidor -> Terminal) 0x35"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comTerminalMealUserManagement(hex_data, server):
    print "Gerenciamento das refeições dos usuários no terminal \
    (Servidor -> Terminal) 0x36"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comSmartCardLayoutSetting(hex_data, server):
    print "Definição do layout do SmartCard \
    (Servidor -> Terminal) 0x40"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comWiegandCommunicationSetting(hex_data, server):
    print "Definição da comunicação da porta Wiegand \
    (Servidor -> Terminal) 0x41"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comTerminalAccessAuthoritySetting(hex_data, server):
    print "Definição da hierarquia de acesso no terminal \
    (Servidor -> Terminal) 0x42"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comEmergencyAlarmSetting(hex_data, server):
    print "Definição do alarme de emergência \
    (Servidor -> Terminal) 0x51"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


def comAnnouncementMessageSending(hex_data, server):
    print "Enviando mensagem pública aos terminais \
    (Servidor -> Terminal) 0x53"
    """
    Rotina para envio de pacote de Logon do Terminal
    (Terminal -> Servidor) código do comando 0x01
    :Return: Datagrama para envio pelo servidor
    :Parameters: Pacote binário no formato Hexadecimal e o
    endereço IP do servidor
    """


options = {
           '01': comTerminalLogon,
           '02': comTerminalLogoff,
           '06': comTCardSerialNReading,
           '09': comTimeSync,
           '0a': comSendingTerminalStatus,
           '13': comSendingAuthResult,
           '29': comCheckUserDuplication,
           '34': comBringMealDataSum,
           '1a': comBringAntipassBackInfo,
           '1b': comBringUserAuthInfo,
           '1c': comServerAuth,
           '60': comNCNOSignalAlarm,
           '05': comSettingTerminalOption,
           '07': comSCardSerialNReading,
           '08': comTerminalTimeSetting,
           '0c': comForceOpenTerminalLock,
           '0d': comControlTerminalPeripheralDevice,
           '16': comBringTerminalAuthRecord,
           '17': comBringTerminalAuditLog,
           '20': comUpgradeTerminalFirmware,
           '21': comBringTerminalFirmwareVersion,
           '27': comTerminalUserSync,
           '33': comSettingTerminalMealOption,
           '35': comShinsegyeTerminalMealUserManagement,
           '36': comTerminalMealUserManagement,
           '40': comSmartCardLayoutSetting,
           '41': comWiegandCommunicationSetting,
           '42': comTerminalAccessAuthoritySetting,
           '51': comEmergencyAlarmSetting,
           '53': comAnnouncementMessageSending,
}
