# xmlParsiewer: XML Parser & Viewer

XML, short for EXtensible Markup Language, is a popular format for storing information and data and representing it as a tree-like structure, and parsers can help visualize said information

Our GUI (Graphical User Interface) parses and visualizes XML files that represent social networks, where users are recorded: each user has a name, a unique ID, possibly a list of posts with their respective topics, and possibly a list of followers with their respective IDs.

## Brief summary of Parsiewer

![image](https://github.com/mohamedAdhamc/xmlParsiewer/assets/90795679/be85cf62-3214-4330-8a72-da4ec1435372)

On the left side is the input text box, as well as the “Import File” button, which does exactly that. On the right side is the output text box, and the “Save File” button. That much is obvious, but there’s much more to say about the middle section, the heart of the app.

In the following sections we will explore the main functions of the app. 

1. GUI features:

   A) Minify:
   his feature expects a syntax-error free XML file from user and returns a new XML file without any redundant spaces or newlines. It supports mixed-elements (tags that have both element children as well as text content)[2] and it supports tag attributes, it also supports self-closing tags and handles XML comments.

   ![image](https://github.com/mohamedAdhamc/xmlParsiewer/assets/90795679/ed0f7ec9-0e42-409b-821d-0c01606d15a1)


   B) Prettify:
   This function adds newlines and tabs to an XML document to make it readable. This can be used to reformat files with messy indentation and redundant newlines. 

   ![image](https://github.com/mohamedAdhamc/xmlParsiewer/assets/90795679/d202e2b6-35b8-4f03-9fc4-a13c22c2cdb9)


3. XML to JSON:

   JSON is another popular format for storing data, and a tool that can convert between XML and JSON would be useful. This is exactly what this does. It accepts any XML file with correct syntax, and outputs the corresponding JSON representation.

   ![image](https://github.com/mohamedAdhamc/xmlParsiewer/assets/90795679/3695ff3c-906c-4a8b-a051-fbb4cd0fd313)


4. Compression and decompression:

   Compression is implemented using the “Byte Pair Encoding” lossless technique. BPE offers a high compression ratio and moderate processing time. It works by scanning through the input text, and finding the most common pair of characters. The most frequent is replaced by a single new character. This process is repeated until the text is no longer compressible (i.e. there are no repeating pairs), or the available character space is depleted.

5. Error detection and correction:

   A) Error detection:
   This checks if there were any closed tags, opening tags or unmatched tags. The xml_error_detection function takes xml_string as an input then checking its consistency then the output of the function is a string contains errors that was found in xml_string.

   ![image](https://github.com/mohamedAdhamc/xmlParsiewer/assets/90795679/4b148f5f-ca8d-45b7-a578-e1c6aa870d4c)


   B) Error correction:
   This function corrects the errors (missing opening or closing tags) in a syntax-error-free XML file. If there are no errors, the output is just the prettified input.

   ![image](https://github.com/mohamedAdhamc/xmlParsiewer/assets/90795679/2282893d-d7f3-46e8-aee9-d2e9658ef426)


7. Social graph analysis:

   A) Build social graph:
   This is an essential step to any of the following features. It optimizes computation time instead of re-building the social graph on every function call.

   B) Visualize social graph:
   Using matplotlib, the user can visualize the built social graph where the connections between different users (who follows whom) are represented using lines and arrowheads.

   ![image](https://github.com/mohamedAdhamc/xmlParsiewer/assets/90795679/4f94d2c7-4fc5-47a3-9289-e0f324236242)


   C) Search posts by topic:
   This allows the user to find all posts that are on a specific topic. The user can enter the preferred topic in the entry box below the button. For the example below, user entered “economy”.

   D) Network analysis:
   Network analysis includes finding the most influential and active users, mutual followers, suggested follows, and searching posts by topic using various graph and user methods. Output is best shown by example, entry boxes for user IDs are provided, in this example, the user entered 2 and 3:

   ![image](https://github.com/mohamedAdhamc/xmlParsiewer/assets/90795679/1feebd41-74ce-43d2-b2a6-24da54f19682)


9. Undo and redo:

   Little needs to be said here. Undo and redo are implemented internally via a stack, and every change to the input text is recorded. Note that changes only count after an enter has been pressed.
