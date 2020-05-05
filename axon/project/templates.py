# -*- coding: utf-8 -*-
"""Template module.

This module manages template creation for automatic generation of code.
Templating is useful to avoid writing boilerplate code and ease development.
"""
import os
import jinja2

TEMPLATE_SUBDIRECTORY = 'templates'
TEMPLATE_FOLDER = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    TEMPLATE_SUBDIRECTORY)

TEMPLATE_LOADER = jinja2.FileSystemLoader(TEMPLATE_FOLDER)
TEMPLATE_ENVIRONMENT = jinja2.Environment(loader=TEMPLATE_LOADER)


def get_template(name):
    """Get template by name."""
    return TEMPLATE_ENVIRONMENT.get_template(name)
