@echo off

rem 仮想環境のパスを指定（仮想環境がプロジェクトフォルダ内にある場合）
set VENV_PATH=.\venv

rem 仮想環境をアクティベート
call %VENV_PATH%\Scripts\activate

rem Pythonスクリプトを実行
python main.py

rem 仮想環境をディアクティベート
call deactivate
