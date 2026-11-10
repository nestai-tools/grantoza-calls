"""Local Git repositories for independent application workspaces."""
import argparse
import os
from pathlib import Path
import subprocess

IGNORE = '''# Local files; application sources and attachments are shared.
.panel/
.env
.env.*
!.env.example
__pycache__/
*.py[cod]
.DS_Store
*.tmp
.panel-*
90-export/
'''
ATTRIBUTES = '''* text=auto
*.md text eol=lf
*.json text eol=lf
*.puml text eol=lf
*.pdf binary
*.docx binary
*.xlsx binary
*.zip binary
*.png binary
'''


def git(path, *args, check=True, env=None, timeout=30):
    environment = dict(os.environ, GIT_TERMINAL_PROMPT='0', GIT_EDITOR='true', LC_ALL='C')
    if env:
        environment.update(env)
    result = subprocess.run(['git', '-C', str(path), '-c', 'protocol.ext.allow=never', *args],
                            capture_output=True, env=environment, timeout=timeout)
    if check and result.returncode:
        raise ValueError(result.stderr.decode('utf-8', 'replace').strip() or 'Operacja Git nie powiodła się.')
    return result


def repository(path):
    path = Path(path).resolve()
    result = git(path, 'rev-parse', '--show-toplevel', check=False)
    return result.returncode == 0 and Path(os.fsdecode(result.stdout).strip()).resolve() == path


def initialize_repository(path, message='Rozpoczęcie pracy nad wnioskiem', defaults=True):
    """Create an independent repo and initial commit, without committing later edits."""
    path = Path(path).resolve()
    path.mkdir(parents=True, exist_ok=True)
    if not (path / '.git').exists():
        git(path, 'init', '-b', 'main')
    if not repository(path):
        raise ValueError('Folder musi mieć własne repozytorium Git.')
    if defaults:
        for name, content in (('.gitignore', IGNORE), ('.gitattributes', ATTRIBUTES)):
            target = path / name
            if not target.exists():
                target.write_text(content, encoding='utf-8')
    if git(path, 'rev-parse', '--verify', 'HEAD', check=False).returncode:
        for setting in ('user.name', 'user.email'):
            if not git(path, 'config', '--get', setting, check=False).stdout.strip():
                raise ValueError(f'Repozytorium utworzono. Ustaw git config {setting}, aby wykonać pierwszy commit, i ponów polecenie.')
        git(path, 'add', '--all')
        git(path, 'commit', '-m', message)
    return git(path, 'rev-parse', 'HEAD').stdout.decode().strip()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    print(initialize_repository(args.folder))
