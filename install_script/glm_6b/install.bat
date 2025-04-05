rem overriding default python env vars in order not to interfere with any system python installation
set PYTHON_PATH=.\py311\
rem overriding default python env vars in order not to interfere with any system python installation
SET PYTHONHOME=
SET PYTHONPATH=
SET PYTHONEXECUTABLE=%PYTHON_PATH%\python.exe
SET PYTHONWEXECUTABLE=%PYTHON_PATHpythonw.exe
SET PYTHON_EXECUTABLE=%PYTHON_PATH%python.exe
SET PYTHONW_EXECUTABLE=%PYTHON_PATH%pythonw.exe
SET PYTHON_BIN_PATH=%PYTHON_EXECUTABLE%
SET PYTHON_LIB_PATH=%PYTHON_PATH%\Lib\site-packages
SET FFMPEG_PATH=%cd%\py311\ffmpeg\bin
SET PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%FFMPEG_PATH%;%PATH%
set HF_ENDPOINT=https://hf-mirror.com
set HF_HOME=%CD%\hf_download
"%PYTHON_EXECUTABLE%" -m pip install --upgrade pip
"%PYTHON_EXECUTABLE%" -m pip install --upgrade -r requirements.txt
"%PYTHON_EXECUTABLE%" -m pip install --upgrade transformers==4.27.1
exit
