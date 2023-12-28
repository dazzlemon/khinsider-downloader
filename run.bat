@echo off

for %%I in ("%~dp0.") do set "script_dir=%%~fI"

set "start_url=%1"
shift

set "PYTHONPATH=%PYTHONPATH%;%script_dir%\src"

@echo on
scrapy runspider %script_dir%\src\spider.py -a start_url=%start_url% %*
