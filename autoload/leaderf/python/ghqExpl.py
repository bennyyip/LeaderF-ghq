#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from leaderf.utils import *
from leaderf.explorer import *
from leaderf.manager import *

_root = lfEval("system('ghq root')[:-2]")


# *****************************************************
# GhqExplorer
# *****************************************************
class GhqExplorer(Explorer):
    def __init__(self):
        self._content = []

    def getContent(self, *args, **kwargs):
        if self._content:
            return self._content
        else:
            return self.getFreshContent()

    def getFreshContent(self, *args, **kwargs):
        repos = lfEval("system('ghq list')").split()

        # github.com/tamago324/LeaderF-ghq
        # <---------/-------------------->
        contents = [r.split("/", 1) for r in repos]

        max_repo_len = max(
            int(lfEval("strdisplaywidth('%s')" % escQuote(item[1])))
            for item in contents
        )

        lines = []

        for service, repo in contents:
            space_num = max_repo_len - int(
                lfEval("strdisplaywidth('%s')" % escQuote(repo))
            )
            lines.append('%s%s "%s"' % (repo, " " * space_num, service))

        self._content = lines

        return self._content

    def getStlCategory(self):
        return "Ghq"

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))

    def supportsNameOnly(self):
        return True


# *****************************************************
# GhqExplManager
# *****************************************************
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
        if cmd == "":
            cmd = "lcd"
        repo = self._getDigest(args[0], 1)
        service = self._getDigest(args[0], 2)
        lfCmd(cmd + " " + os.path.join(_root, os.path.join(service, repo)))

    def _getDigest(self, line, mode):
        """
        specify what part in the line to be processed and highlighted
        Args:
            mode: 0, return the full path
                  1, return the name only
                  2, return the directory name
        """
        if not line:
            return ""
        if mode == 0:
            return line
        elif mode == 1:
            start_pos = line.find(' "')
            return line[:start_pos].rstrip()
        else:
            start_pos = line.find(' "')
            return line[start_pos + 2 : -1]

    def _getDigestStartPos(self, line, mode):
        """
        specify what part in the line to be processed and highlighted
        Args:
            mode: 0, return the full path
                  1, return the name only
                  2, return the directory name
        """
        if not line:
            return 0

        if mode == 2:
            start_pos = line.find(' "')
            return lfBytesLen(line[: start_pos + 2])
        else:
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

    def _afterEnter(self):
        super(GhqExplManager, self)._afterEnter()
        if self._getInstance().getWinPos() == "popup":
            lfCmd(
                """call win_execute(%d, 'let matchid = matchadd(''Lf_hl_ghqServiceName'', ''\s\+\zs".\+'')')"""
                % self._getInstance().getPopupWinId()
            )
            id = int(lfEval("matchid"))
            self._match_ids.append(id)
        else:
            id = int(lfEval("matchadd('Lf_hl_ghqServiceName', '\s\+\zs" ".\+')"))
            self._match_ids.append(id)


# *****************************************************
# ghqExplManager is a singleton
# *****************************************************
ghqExplManager = GhqExplManager()

__all__ = ["ghqExplManager"]
