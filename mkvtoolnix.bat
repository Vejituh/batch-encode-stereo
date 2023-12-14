@echo off

if not exist "out" (
    mkdir "out"
)

if exist "options.json" (
  for %%f in (*.mkv) do (
    mkvmerge @options.json -o "out/%%f" "%%f" 
    del "%%f"
  )
) else (
  for %%I in (*) do (
    if not "%%I"=="mkvtoolnix.bat" (
        move "%%I" out\
    )
)
  goto afterForLoop
)

call :afterForLoop
exit /b

:afterForLoop
    echo Starting Encode

    cd out
    copy "C:\Users\Vejituh\Documents\batch_encoder.py" "."
    python batch_encoder.py
    
    cd ..
    pause
exit /b