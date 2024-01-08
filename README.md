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

   B) Prettify:
   This function adds newlines and tabs to an XML document to make it readable. This can be used to reformat files with messy indentation and redundant newlines. 

3. XML to JSON:

   JSON is another popular format for storing data, and a tool that can convert between XML and JSON would be useful. This is exactly what this does. It accepts any XML file with correct syntax, and outputs the corresponding JSON representation.

5. Compression and decompression:

6. Error detection and correction:

7. Social graph analysis:

8. Undo and redo:


## Supporting data structures and classes


