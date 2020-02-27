# -*- coding: utf-8 -*-
"""
Run command.

This command excutes python scripts but will track all produced information
to MLFlow and DVC.

Should point to a script file and read any sources of data or other code
dependencies and data outputs, and use them to run:

dvc run script -d dependencies -o outputs
"""
