def XML_error_detector(xml):
    i=0
    open=[]  
    closed=[] 
    errors=[]
    closing=False
    error_string=""

    while i < len(xml):
        if xml[i] == "<":
            if xml[i+1] != "/":  
                i+=1
                open_tag=""
                while xml[i] != ">":
                    open_tag+=xml[i]
                    i+=1
                closing=False 

                open_tag_content=open_tag.replace("<", '').replace(">", '')
                open.append(open_tag_content)
            elif xml[i+1] == "/":
                i+=2
                closed_tag=""
                while xml[i] != ">":
                    closed_tag+=xml[i]
                    i+=1
                closing=True
            
                closed_tag_content=closed_tag.replace("<", '').replace("/", '').replace(">", '')
                closed.append(closed_tag_content)

        if closing and open:
            exsit=True
            if open and closed and closed[-1]!=open[-1]:
                while open and exsit :
                    for element in open:
                        if element == closed[-1]:
                            exsit=True
                            break
                    else:
                        exsit=False
                    if exsit:
                        errors.append(open.pop())
                        if open and closed and open[-1] == closed[-1]:
                            closed.pop()
                            open.pop()
                            while errors:
                              error_string += f"Missing closed tag for opening tag: {errors.pop()}\n"
                            break
                    else:
                        unmatched_tag = closed.pop()
                        error_string += f"Unmatched tag for opening tag {open[-1]}: {unmatched_tag}\n"
                        
                    
                while errors:
                    open.append(errors.pop())
                    
                if closed:
                    error_string += f"{closed[-1]} tag is not opened\n"
                    closed.pop()
                
            else:
                open.pop()
                if closed:
                    closed.pop()
            closing = False
            
        i+=1

    while open:
        error_string += f"{open.pop()} tag is not closed\n"

    while closed:
       error_string += f"{closed.pop()} tag is not opened\n"
    
    if(error_string):
        return error_string
    else:
        return "correct XML file "


