import subprocess
subprocess.call(['git', 'add', '-A'])
subprocess.call(['git', 'commit', '-m', '{}'.format('routine update')])
subprocess.call(['git', 'push', 'https://NixonCTChan:{}@github.com/NixonCTChan/Thermal.git'.format('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')])

