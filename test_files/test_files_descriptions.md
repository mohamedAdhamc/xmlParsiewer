# Test Files Descriptions

\# |File name | Description
--- | --- | ---
1 | generic_syntactically_correct1.xml | This file tests all sorts of corner cases for minify, prettify, xml2json, and compression functions. Its syntax is correct, although it lacks general meaning so it can't be used for other funcions, and it's not even valid XML. Just correct syntax.
2 | generic_syntactically_correct2.xml | This is similar to the above file, but it's large in size to test performance of the app and confirm calculated complexity. It's around 2,000,000 characters, and 60,000 lines.
3 | generic_syntactically_correct3.xml | This is similar to the above files, but it's much, much larger. Extremely large that it's difficult to load or edit on text editors. It's around 20,000,000 characters, and 600,000 lines. This is to test the functions on their own and it performs each of them within a few seconds, but it gets sluggish when scrolling through the text boxes on the GUI (specifically when scrolling through minify's output horizontally).
4 | repeated_elements.xml | Yet again, another correct-but-not-valid test file. This is to test that parsing for minify, prettify, and xml2json is done correctly on repeated elements within an element's children, as well as elements that share a name with their parents.
5 | sample_input.xml | The sample input file given in the project description as an example. The file syntax as well as meaning is correct.
6 | sample_input.xml | The sample input file with mistakes in it to test error detection and correction.
7 | sample_input_users_network.xml | The sample input file given in the project description as an example for visualization.
