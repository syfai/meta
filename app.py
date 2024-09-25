import subprocess, os, shutil, time, sys, platform, stat
if platform.system() == 'Windows':
    raise SystemError("You are trying to run this demo on **Windows**. Windows is not supported. If you would still like to try, remove lines 2 & 3 in the code to bypass this warning.")

def setup_virtual_env():
    # Create a virtual environment directory
    subprocess.run(['python', '-m', 'venv', './venv_ui'])
    
    # Activate the virtual environment
    activate_script = os.path.join('venv_ui', 'bin', 'activate')
    
    st = os.stat(activate_script)
    os.chmod(activate_script, st.st_mode | stat.S_IEXEC)
    subprocess.run([activate_script], shell=True)

    # Install required packages
    subprocess.run(['pip', 'install', 'gradio', 'requests'])

def move_files_and_subdirs(source_dir):
    # List all files and directories in the source directory
    files_and_dirs = os.listdir(source_dir)
    
    # Move each file and directory to the current working directory
    for item in files_and_dirs:
        # Get the full path of the item
        src_path = os.path.join(source_dir, item)
        # Check if it's a file
        if os.path.isfile(src_path):
            # Move the file to the current working directory
            shutil.move(src_path, os.path.join(os.getcwd(), item))
        elif os.path.isdir(src_path):
            # Move the directory and its contents recursively to the current working directory
            shutil.move(src_path, os.path.join(os.getcwd(), item))
        else:
            print(f"Ignoring: {src_path} as it is neither a file nor a directory")


subprocess.run(['git', 'clone', 'https://github.com/fakerybakery/metavoice-src', './mvsrc'])
time.sleep(3)
subprocess.run(['pip', 'uninstall', '-y', 'pydantic', 'spacy'])
subprocess.run(['pip', 'install', '-U', 'fastapi', 'spacy', 'transformers', 'flash-attn'])
move_files_and_subdirs("mvsrc")
time.sleep(3)
serving = subprocess.Popen(['python', 'fam/llm/serving.py', '--huggingface_repo_id', 'metavoiceio/metavoice-1B-v0.1'])
# subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
setup_virtual_env()
subprocess.run(['python', 'fam/ui/app.py'])
# subprocess.run(['deactivate'], shell=True)

serving.communicate()