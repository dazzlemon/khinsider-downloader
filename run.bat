@echo off

for %%I in ("%~dp0.") do set "script_dir=%%~fI"

set "file_path=%1"
set "PYTHONPATH=%PYTHONPATH%;%script_dir%\src"

set "remaining_args=%*"
set "remaining_args=%remaining_args:* =%"

@echo on
scrapy runspider %script_dir%\src\spider.py -a file_path=%file_path% %remaining_args%
