REM Mac
REM pyinstaller --noconfirm --windowed --clean --log-level=WARN \
REM             --onefile --version-file=version.txt \
REM             --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' \
REM             --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' \
REM             --name="PAR WorkSchedule" --icon=bil.icns Workschedule.py

REM Windows
pyinstaller --noconfirm --nowindow --clean --log-level=WARN ^
    --onefile --version-file=version.txt ^
    --name="PAR WorkSchedule" --icon=bil.ico ^
    Workschedule.py