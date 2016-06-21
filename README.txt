Language: Python 3.5.1
https://www.python.org/downloads/

I'm using Sublime Text 3, 
https://www.sublimetext.com/3
but the editor is up to personal preference.

To build a Python 3.5 file with Sublime 3, you need to add a build system
Go to tools -> build system -> new build system. 
Delete the code there and paste. NOTE: Replace "585802" with your Booz Allen ID

{
"cmd": ["C:\\Users\\585802\\AppData\\Local\\Programs\\Python\\Python35\\python", "-u", "$file"],
"file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
"selector": "source.python"
}

the line next to "cmd" is the location of python.exe on your computer, which could vary but this should be the default.
Save this file at the default location, ending your file name with .sublime-build

Then, create a new file, write
print("hi")
Save the file as test.py wherever you want.
Press ctrl-B to build, you should see hi appear at the bottom and that's how you know if python has been installed correctly.



We're using Github for collaboration and version control.
https://github.com/brandonisthebomb/Entertainment-Analytics

Install these packages:
	- 	pip for easy downloads, then use 'pip install putmodulehere' to install
		various modules. You might need to use the command prompt. The path to pip is 
		C:\Users\585802\AppData\Local\Programs\Python\Python35\Scripts

	-	Locate pip (go to the folder with pip.exe in it) using the command prompt and type
		pip install beautifulsoup4 
		https://www.crummy.com/software/BeautifulSoup/bs4/doc/

	- 	The urllib package doesn't need to be installed

	-	For a database solution that works well with python and uses Maria.db
		http://stackoverflow.com/questions/32036119/beautiful-soup-webscrape-into-mysql
		https://github.com/PyMySQL/PyMySQL#example
		pip install PyMySQL

		Read the getting started section to learn more about SQL and relational databases in general.
		https://mariadb.org/learn/

	

