import os
import subprocess

# ...existing code...

def setup_environment():
    # Create virtual environment
    subprocess.run(['python3', '-m', 'venv', 'venv'])

    # Activate virtual environment
    activate_script = './venv/bin/activate' if os.name != 'nt' else '.\\venv\\Scripts\\activate'
    subprocess.run(['source', activate_script], shell=True)

    # Install dependencies
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

    # Create .gitignore file
    with open('.gitignore', 'w') as gitignore:
        gitignore.write('.env\n')
        gitignore.write('venv\n')

if __name__ == "__main__":
    setup_environment()

# ...existing code...
