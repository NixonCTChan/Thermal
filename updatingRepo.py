import subprocess
subprocess.call(['git', 'add', '-A'])
subprocess.call(['git', 'commit', '-m', '{}'.format('routine update')])
subprocess.call(['git', 'push', 'https://NixonCTChan:{}@github.com/NixonCTChan/Thermal.git'.format('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')])

