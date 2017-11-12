#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vim
import subprocess
from leaderf.utils import *
from leaderf.explorer import *
from leaderf.manager import *

import os

_root = subprocess.run(
    ['ghq', 'root'],
    check=True,
    universal_newlines=True,
    stdout=subprocess.PIPE).stdout.strip()


#*****************************************************
# GhqExplorer
#*****************************************************
class GhqExplorer(Explorer):
    def __init__(self):
        self._content = []

    def getContent(self, *args, **kwargs):
        if self._content:
            return self._content
        else:
            return self.getFreshContent()

    def getFreshContent(self, *args, **kwargs):
        cmd = ['ghq', 'list']
        self._content = subprocess.run(
            cmd, check=True, universal_newlines=True,
            stdout=subprocess.PIPE).stdout.split()

        return self._content

    def getStlCategory(self):
        return "ghq"


#*****************************************************
# GhqExplManager
#*****************************************************
class GhqExplManager(Manager):
    def __init__(self):
        super(GhqExplManager, self).__init__()
        self._match_ids = []

    def _getExplClass(self):
        return GhqExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#Ghq#Maps()")

    def _acceptSelection(self, *args, **kwargs):
        if len(args) == 0:
            return
        repo = args[0]
        lfCmd("lcd %s" % os.path.join(_root,repo))
        lfCmd("edit %s" % os.path.join(_root,repo))

    def _getDigest(self, line, mode):
        if not line:
            return ''
        return line

    def _getDigestStartPos(self, line, mode):
        return 0

    def _createHelp(self):
        help = []
        help.append('" <F1> : toggle this help')
        help.append('" <F5> : refresh the cache')
        help.append('" <CR>/<double-click>/o : edit repo')
        help.append('" i : switch to input mode')
        help.append('" q : quit')
        help.append(
            '" ---------------------------------------------------------')
        return help

    def _beforeExit(self):
        super(GhqExplManager, self)._beforeExit()
        for i in self._match_ids:
            lfCmd("silent! call matchdelete(%d)" % i)
        self._match_ids = []


#*****************************************************
# ghqExplManager is a singleton
#*****************************************************
ghqExplManager = GhqExplManager()

__all__ = ['ghqExplManager']
