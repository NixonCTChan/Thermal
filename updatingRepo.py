import subprocess
subprocess.call(['git', 'add', '-A'])
subprocess.call(['git', 'commit', '-m', '{}'.format('routine update')])
subprocess.call(['git', 'push', 'https://{}@github.com/NixonCTChan/Thermal.git'.format('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')])

