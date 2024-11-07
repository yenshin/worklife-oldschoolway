# note for worklife examinator
app.env 
	I remove the credential data to not have it in git
	(test system is often use as an entry point for malicious person)
	
	here command line to avoid update when you modify the file:
		git update-index --assume-unchanged ${file} # to hide file
		git update-index --no-assume-unchanged ${file} # to show back the file
		
library added:
	- debugpy
		allow me to debug with vscode debugger
		don't forget to docker-compose up -d --build

I try to follow this recommendation:
	https://wiki.postgresql.org/wiki/Don't_Do_This
	
note: work with python 3.11
	