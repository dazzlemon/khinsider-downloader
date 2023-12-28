@echo off

for %%I in ("%~dp0.") do set "script_dir=%%~fI"

set "start_url=%1"
set "PYTHONPATH=%PYTHONPATH%;%script_dir%\src"

set "remaining_args=%*"
set "remaining_args=%remaining_args:* =%"

@echo on
scrapy runspider %script_dir%\src\spider.py -a start_url=%start_url% %remaining_args%
