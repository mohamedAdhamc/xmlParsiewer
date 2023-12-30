def XML_error_detector(xml):
    """
    Detect errors in an XML string and return error messages with line numbers.

    Parameters:
    - xml (str): The input XML string to be checked for errors.

    Returns:
    - str: A string containing error messages with line numbers, or a message indicating
           that the XML file is correct if no errors are found.
    """

    i=0
    open=[]  
    closed=[] 
    errors=[]
    closing=False
    error_string=""
    line_number=1

    while i < len(xml):

        if xml[i]=='\n':
            # Increment line number when a newline character is encountered
            line_number += 1

        # Check if the current character is the start of an XML tag
        if xml[i] == "<":
            if xml[i+1] != "/":  
                i+=1
                open_tag=""
                # Extract the content of the opening tag until '>'
                while xml[i] != ">":
                    open_tag+=xml[i]
                    i+=1
                closing=False 
                # Extract the content of the opening tag (excluding '<' and '>')
                open_tag_content=open_tag.replace("<", '').replace(">", '')
                open.append(open_tag_content)

            #The same logic will happen If it's a closing tag
            elif xml[i+1] == "/":
                i+=2
                closed_tag=""
                while xml[i] != ">":
                    closed_tag+=xml[i]
                    i+=1
                closing=True
                closed_tag_content=closed_tag.replace("<", '').replace("/", '').replace(">", '')
                closed.append(closed_tag_content)

        # If there is a closing tag and there are open tags in stacks
        if closing and open:
            exsit=True
            # Check if the last open tag matches the last closed tag
            if open and closed and closed[-1]!=open[-1]:
                # Loop until a matching open tag is found in stack is crossponding to the closed tag in closed stack or no open tags
                while open and exsit :
                    for element in open:
                        if element == closed[-1]:
                            exsit=True
                            break
                    else:
                        exsit=False

                    # If a matching open tag is found,so there is a missing closed tag for the first element in opening tag
                    if exsit:
                        errors.append(open.pop())
                        if open and closed and open[-1] == closed[-1]:
                            closed.pop()
                            open.pop()
                            while errors:
                              error_string += f"Missing closed tag for opening tag: {errors.pop()} at line {line_number}\n"
                            break
                    # if there is no matching tag for the closed tag in the stack in the opening tag so there is missing opening tag or missmatched tag  
                    else:
                        unmatched_tag = closed.pop()
                        error_string += f"Unmatched tag for opening tag : {open[-1]}-> {unmatched_tag}\n"
                        error_string +=f" or missing an opening tag for {unmatched_tag} at line {line_number}\n"
                        
                    
                while errors:
                    open.append(errors.pop())
                # If there are still closed tags report them    
                if closed:
                    error_string += f"{closed[-1]} tag is not opened at line {line_number}\n"
                    closed.pop()
                
            else:
                # If the last open tag matches the last closed tag, pop them
                open.pop()
                if closed:
                    closed.pop()
            closing = False
            
        i+=1
    
    # Process any remaining open or closed tags
    while open:
        error_string += f"{open.pop()} tag is not closed at line {line_number}\n"

    while closed:
       error_string += f"{closed.pop()} tag is not opened at line {line_number}\n"
    
    if(error_string):
        return error_string
    else:
        return "correct XML file "
    

