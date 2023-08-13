pipenv run pyinstaller .\Project.spec
Move-Item .\dist\ProjectName.exe .\ -Force
Remove-Item .\dist -Force -Recurse
Remove-Item .\build -Force -Recurse
