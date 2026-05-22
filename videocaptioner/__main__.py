"""Allow running as: python -m videocaptioner"""

import multiprocessing
import sys

# Required for Windows when packaged as a PyInstaller executable
multiprocessing.freeze_support()

from videocaptioner.cli.main import main

sys.exit(main())
