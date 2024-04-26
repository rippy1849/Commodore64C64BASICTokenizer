import binascii as bs

def hex_convert(num):
    
    h = hex(num)[2:]
    if len(h) % 2 == 1:
        h = '0' + h
    
    #Flip into lobyte-hibyte order
    if len(h) == 4:
        p1 = h[0:2]
        p2 = h[2:4]
        h = p2 + p1
    return h

def hex_convert_16(num):
    #Convert the line number into 16 bit low-high output
    h = hex(num)[2:]
    if len(h) % 2 == 1:
        h = '0' + h
    if len(h) == 2:
        h = '00' + h
    #Flip into lobyte-hibyte order
    if len(h) == 4:
        p1 = h[0:2]
        p2 = h[2:4]
        h = p2 + p1
    return h








#starting bytecode

def LineCase(entry):
    
    
    bstring = b''
    lp = 0
    
    #The first part that contains the line number (separate since it requires a 16bit hex conversion)
    #split off first space since it doesn't count in hex
    s = entry.split(" ", 1)
    #convert line number to 16 bit hex
    
    bstring += bs.unhexlify(hex_convert_16(int(s[0])))
    
    #add 2 bytes to the counter for the next line pointer (from the 2 byte line number)
    lp += 2
            
            
    #Can generalize here with key-value library
    #replace the tokens for counting
    for token in TOKEN_LIB:
        s[1] = s[1].replace(token,pad + TOKEN_LIB[token])
                     
        #create empty byte list
    t4 = []
    count = 0
    #convert string into bytes
            
    while count < len(s[1]):

        if s[1][count] == pad:
            t4.append(s[1][count+1] + s[1][count+2])
            count += 3
        else:
            t4.append(str(hex_convert(ord(s[1][count]))))
            count+=1
        #update line pointer
    lp += len(t4)
    #dump the hex
            
    for tok in t4:
        bstring += bs.unhexlify(tok)
    
    return bstring,lp

def TextCase(entry,quoteflag):
    
    bstring = b''
    lp = 0
    #add quotation mark
    if quoteflag:
        bstring += bs.unhexlify('22')
        lp += 1
                
    #convert to tokenized hex
    for e in entry:
        if e == " ":
            bstring += bs.unhexlify('20')
                        
        else:
            bstring += e.encode()
                    
            #update line pointer
        lp += 1
                
    #add quotation mark
    if quoteflag:
        bstring += bs.unhexlify('22')
        lp += 1
    
    return bstring,lp

def TokenCase(entry):
    
    bstring = b''
    lp = 0
    
    s = entry
    #replace the tokens for counting
    for token in TOKEN_LIB:
        s = s.replace(token,pad + TOKEN_LIB[token])
                
    #create empty byte list
    t4 = []
    count = 0
    #convert string into bytes
    while count < len(s):
                
        if s[count] == pad:
            t4.append(s[count+1] + s[count+2])
            count += 3
        else:
            t4.append(str(hex_convert(ord(s[count]))))
            count+=1
    #update line pointer
    lp += len(t4)
                
    #dump the hex
    for tok in t4:
        bstring += bs.unhexlify(tok)
    
    return bstring,lp






output = b'\x01\x08'

remflag = False

#string that will hold raw basic code
basic = ""

#padding, used for counting
pad = "~"

#List of Hex Token specific elements for basic
#TOKEN_LIB = {'PRINT#':'98','PRINT':'99','INPUT#':'84','INPUT':'85','IF':'8B','OPEN':'9F','GET':'A1','CHR$':'C7','THEN':'A7','GOTO':'89','STR$':'C4','CLOSE':'A0','=':'B2','+':'AA','AND':'AF'}

#Library is missing power symbol (AE)
TOKEN_LIB = {'END':'80','FOR':'81','NEXT':'82','DATA':'83','INPUT#':'84',
             'INPUT':'85','DIM':'86','READ':'87','LET':'88','GOTO':'89',
             'RUN':'8A','IF':'8B','RESTORE':'8C','GOSUB':'8D','RETURN':'8E',
             'STOP':'90','ON':'91','WAIT':'92','LOAD':'93','SAVE':'94',
             'VERIFY':'95','DEF':'96','POKE':'97','PRINT#':'98','PRINT':'99',
             'CONT':'9A','LIST':'9B','CLR':'9C','CMD':'9D','SYS':'9E','OPEN':'9F',
             'CLOSE':'A0','GET':'A1','NEW':'A2','TAB(':'A3','TO':'A4','FN':'A5',
             'SPC(':'A6','THEN':'A7','NOT':'A8','STEP':'A9','+':'AA','-':'AB','*':'AC',
             '/':'AD','AND':'AF','OR':'B0','>':'B1','=':'B2','<':'B3','SGN':'B4',
             'INT':'B5','ABS':'B6','USR':'B7','FRE':'B8','POS':'B9','SQR':'BA',
             'RND':'BB','LOG':'BC','EXP':'BD','COS':'BE','SIN':'BF','TAN':'C0',
             'ATN':'C1','PEEK':'C2','LEN':'C3','STR$':'C4','VAL':'C5','ASC':'C6',
             'CHR$':'C7','LEFT$':'C8','RIGHT$':'C9','MID$':'CA','GO':'CB'}

#opens the basic file
with open('input.bas') as f:
    basic = f.readlines()


#Starts at 2048(+4) to account for the x01 x08, the first 16bit line pointer value
line_pointer = 2052

for line in basic:
    #remove line breaks
    line = line.replace("\n", "")

    #split into text & tokens
    parts = line.split("\"")
    
    #filter off occasional extra nothing from split function
    if parts[-1] == "":
        parts.pop(-1)
    #base converted hex

    l = b""
    
    for i,entry in enumerate(parts):
        
        #Check to see if REM is a token
        if 'REM' in entry and i%2==0:
            remflag = True
        
        if remflag:
            if i%2 == 1:
                entry = "\"" + entry + "\""
            rsplit = entry.split("REM",1)
            
            if i == 0:
                bstring,lp = LineCase(rsplit[0])
                l += bstring
                line_pointer += lp
            
            # add case for left of REM, and for right of rem
             
                if len(rsplit) > 1:
                    l += bs.unhexlify('8F')
                    bstring,lp = TextCase(rsplit[1],False)
                    l += bstring
                    line_pointer += lp
            else:
                
                bstring,lp = TextCase(rsplit[0], False)
                l += bstring
                line_pointer += lp
                
                if len(rsplit) > 1:
                    l += bs.unhexlify('8F')
                    bstring,lp = TextCase(rsplit[1],False)
                    l += bstring
                    line_pointer += lp
            
        else: 
            #The first part that contains the line number (separate since it requires a 16bit hex conversion)
            if i == 0:
                bstring,lp = LineCase(entry)
                
                l+=bstring
                line_pointer += lp
                    
            else:
                #in quotes (direct conversion)
                if i % 2 == 1:
                    bstring,lp = TextCase(entry,True)
                    l += bstring
                    line_pointer += lp
                #This is outside of quotes, must use tokenizer conversion
                else:
                    bstring,lp = TokenCase(entry)
                    l += bstring
                    line_pointer += lp
    
    #line is now completely converted, stick the line pointer in
    remflag = False 
    if line != "":
        lp_converted = bs.unhexlify(hex_convert_16(line_pointer))
        l = lp_converted + l + bs.unhexlify('00')
        
        output += l
        line_pointer+=3







    
#end the program
output += bs.unhexlify('0000')
#print(output)
with open('converted.prg', 'wb') as f:
    f.write(output)

    
    
    
    