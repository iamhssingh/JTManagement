from distutils.core import setup

setup(windows=['main.py'],
      name="JTManagement",
      options={'py2exe': {
          "optimize": 2,
          "bundle_files": 2,  # This tells py2exe to bundle everything
      }},
      )
