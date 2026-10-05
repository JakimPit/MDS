"""Execute all notebooks with this project's interpreter and save outputs."""
import json
import os
import sys
import time
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

root = Path(__file__).resolve().parent
os.environ['MPLBACKEND'] = 'module://matplotlib_inline.backend_inline'
results = []
for path in sorted((root / 'MDS-new').glob('HW*.ipynb')):
    start = time.monotonic()
    notebook = nbformat.read(path, as_version=4)
    km = KernelManager(kernel_name='python3')
    # Override the command to avoid picking a global Python kernel.
    km.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
    client = NotebookClient(notebook, km=km, timeout=300, resources={'metadata':{'path':str(path.parent)}})
    try:
        client.execute()
        nbformat.write(notebook, path)
        result = {'notebook':path.name,'status':'passed','seconds':round(time.monotonic()-start,2)}
        print(json.dumps(result),flush=True)
        results.append(result)
    finally:
        if km.has_kernel:
            km.shutdown_kernel(now=True)
(root / 'verification.json').write_text(json.dumps({'verified_on':'2026-10-05','python':sys.version.split()[0],'results':results},indent=2)+'\n',encoding='utf-8')
