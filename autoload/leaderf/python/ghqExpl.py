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
        self._executor = []

    def getContent(self, *args, **kwargs):
        cmd = 'ghq list'
        executor = AsyncExecutor()
        self._executor.append(executor)
        return executor.execute(cmd, encoding=lfEval("&encoding"))

    def getStlCategory(self):
        return "Ghq"

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))

    def cleanup(self):
        for exe in self._executor:
            exe.killProcess()
        self._executor = []


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
        cmd = lfEval("g:Lf_GhqAcceptSelectionCmd")
        if cmd == '':
            cmd = 'lcd'
        repo = args[0]
        lfCmd(cmd + ' ' + os.path.join(_root, repo))

    def _getDigest(self, line, mode):
        if not line:
            return ''
        return line

    def _getDigestStartPos(self, line, mode):
        return 0

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : execute command under cursor')
        help.append('" i : switch to input mode')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" <F5> : refresh the cache')
        help.append('" ---------------------------------------------------------')
        return help


#*****************************************************
# ghqExplManager is a singleton
#*****************************************************
ghqExplManager = GhqExplManager()

__all__ = ['ghqExplManager']
