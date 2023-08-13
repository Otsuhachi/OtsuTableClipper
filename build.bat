pipenv run pyinstaller .\Project.spec
move /y .\dist\ProjectName.exe .\
rmdir /s /q .\dist\
rmdir /s /q .\build
