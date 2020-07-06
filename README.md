This utility is designed as a tool to aid me in the development of my card game 'Too Greedily, Too Deep'. Ultimately it will be able to read values out of a csv file and create an array of images which can be used for rapid prototyping in online board game systems.

HOW TO:

Card Sharp is a command line python script that extracts data from a csv file and compiles it into an array of simple png cards containing text, numbers and horizontal rules, using one of a set of rules to create the card layout. The layout schema is described in layouts.txt in the Layouts folder.

To run Card Sharp you must have python 3.8.3+ installed. Card Sharp also uses the Pillow 7.2.0 image library.

Card Sharp requires the name of the csv file minus the extension (ie 'target') and either -i (to output image files) or -t (to output text files). -h will give other optional command line arguments.

Though Card Sharp is currently crude it should be possible to use it for your own projects if you do so wish, and development is ongoing.

CONFIG.INI:

Many specifics of how the cards will be set up, including font names, font sizes, the specific RGB values associated with colours and the column of the CSV from which the Layout names are read, are customisable in the config.ini file. 
