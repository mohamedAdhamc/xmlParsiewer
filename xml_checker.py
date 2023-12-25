def XML_Check(xml): # correct version i made
    i=0
    open=[]  # d open
    closed=[] # c
    errors=[]#change variable name later
    closing=False
    while i < len(xml):
        if xml[i] == "<":
            if xml[i+1] != "/": # if is not a closing tag 
                i+=1
                open_tag=""
                while xml[i] != ">":
                    open_tag+=xml[i]
                    i+=1
                closing=False # i think it will not affect if it is removed

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
                              print("Missing closed tag for opening tag :",errors.pop())
                            break
                    else:
                        unmatched_tag = closed.pop()
                        print(f"Un matched tag for opening tag {open[-1]}: {unmatched_tag}")
                        
                    
                while errors:
                    open.append(errors.pop())
                    
                if closed:
                    print(closed[-1],"tag is not opened")
                    closed.pop()
                
            else:
                open.pop()
                if closed:
                    closed.pop()
            closing = False
            
        i+=1

    while open:
        print(open.pop(), "tag is not closed")

    while closed:
        print(closed.pop(), "tag is not opened")
    
                  
xml_string = """
<users>
    <user>
        <id>1
        <name>Ahmed Ali</name>
        <posts>
            <post>
                <body>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                </body>
                <topics>
                    <topic>
                        economy
                    </topic>
                    <topic>
                        finance
                    </topic>
                </topics>
            </post>
            <post>
                <body>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                </body>
                <topics>
                    <topic>
                        solar_energy
                    </topic>
                </topics>
            </post>
        </posts>
        <followers>
            <follower>
                <id>2</id>
            </follower>
            <follower>
                <id>3</name>
            </follower>
        </followers>
    </user>
    <user>
        <id>2</id>
        <name>Yasser Ahmed</name>
        <posts>
            <post>
                <body>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                </body>
                <topics>
                    <topic>
                        education
                    </topic>
                </topics>
            </post>
        </posts>
        <followers>
            <follower>
                <id>1</id>
            </follower>
        </followers>
    </user>
    <user>
        <id>3</id>
        <name>Mohamed Sherif</name>
        <posts>
            <post>
                <body>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                </body>
                <topics>
                    <topic>
                        sports
                    </topic>
                </topics>
            </post>
        </posts>
        <followers>
            <follower>
                <id>1</id>
            </follower>
       
    </user>
</users>
"""
XML_Check(xml_string)



