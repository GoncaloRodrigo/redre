import socket
import sys

space = ' '
endLine = '\n'
nullStr = ''
arrow = '-> '

invalidUsage = 'Invalid Usage: python TCS.py -p <portNumber>'
portSet = '-p'

langs = []

regSvr = 'SR'
unregSvr = 'SU'
userSvrAddr = 'UN'
userList = 'UL'
statusReply = 'R '

statusOK = 'OK'
statusKO = 'NOK'
statusERR = 'ERR'
statusEOF = 'EOF'

def validateIp(ipStr):
    ip = ipStr.split('.')
    if len(ip) != 4:
        return False
    for part in ip:
        if not part.isdigit():
            return False
        
        number = int(part)
        if number < 0 or number > 255:
            return False
    return True

def validatePort(port):
    try:
        portNo = int(port)
        
        if portNo > 0:
            return True
        return False
    except ValueError:
        return False

def validateCmd(cmd, cmdArgs, argCount):
    global response
    valid = True
    response = cmd + statusReply
 
    if argCount == 0:
        return True
    
    else:
        if argCount == len(cmdArgs):
            if cmdArgs[0].strip().isalpha():
                found = False
                info = nullStr
                
                for lang in langs:
                    if cmdArgs[0].strip().upper() == lang.split(space, 1)[0].strip().upper():
                        found = True
                        info = lang.split(space, 1)[1].strip()
                    
                if not found and cmd != regSvr:
                    if cmd == unregSvr:
                        response += statusKO
                    elif cmd == userSvrAddr:
                        response += statusEOF
                    return False
                else:
                    if cmd == regSvr and str(cmdArgs[1] + space + cmdArgs[2]).strip() == info:
                        response += statusKO
                        return False
            else:
                valid = False
            
            if len(cmdArgs) > 1:
                if not validateIp(cmdArgs[1]):
                    valid = False
            
            if len(cmdArgs) > 2:
                if not validatePort(cmdArgs[2]):
                    valid = False
                    
        if not valid:
            response += statusERR
        return valid


serverPort = 58004
if len(sys.argv) > 1:
    if sys.argv[1] == portSet and validatePort(sys.argv[2]):
        serverPort = int(sys.argv[2])
    else:
        print(invalidUsage)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverAddress = (socket.gethostbyname(socket.getfqdn()), serverPort)

sock.bind(serverAddress)

while True:
    data, address = sock.recvfrom(4096)

    if data:
        recv = data.decode()
        cmd = recv.split(space, 1)
        cmdArgs = []
        response = nullStr
                
        if(len(cmd) > 1):
            cmdArgs = cmd[1].split(space)
            
        logMsg = cmd[0].strip() + space
        for arg in cmdArgs:
            logMsg += arg.strip() + space
        logMsg += arrow + str(address[0]) + space + str(serverPort)
        print(logMsg)
        
        if cmd[0].upper().startswith(regSvr):
            if validateCmd(regSvr, cmdArgs, 3):
                langs.append(cmd[1])
                response += statusOK
                
        elif cmd[0].upper().startswith(unregSvr):
            if validateCmd(unregSvr, cmdArgs, 3):
                langs.remove(cmd[1])
                response += statusOK
                
        elif cmd[0].upper().startswith(userList):
            if validateCmd(userList, cmdArgs, 0):
                response += str(len(langs))
            
                for lang in langs:
                    langName = lang.split(space, 1)
                    response += space + langName[0]
                    
        elif cmd[0].upper().startswith(userSvrAddr):
            if validateCmd(userSvrAddr, cmdArgs, 1):      
                for lang in langs:
                    langSvr = lang.split(space, 1)
                
                    if langSvr[0].upper().strip() == cmd[1].upper().strip():
                        response += langSvr[1]
                        break
        else:
            response += statusERR
        
        response += endLine
        sock.sendto(response.encode(), address)
        
