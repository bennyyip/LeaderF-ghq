if leaderf#versionCheck() == 0
    finish
endif

exec g:Lf_py "import vim, sys, os.path"
exec g:Lf_py "cwd = vim.eval('expand(\"<sfile>:p:h\")')"
exec g:Lf_py "sys.path.insert(0, os.path.join(cwd, 'python'))"
exec g:Lf_py "from ghqExpl import *"

function! leaderf#Ghq#Maps()
    nmapclear <buffer>
    nnoremap <buffer> <silent> <CR>          :exec g:Lf_py "ghqExplManager.accept()"<CR>
    nnoremap <buffer> <silent> o             :exec g:Lf_py "ghqExplManager.accept()"<CR>
    nnoremap <buffer> <silent> <2-LeftMouse> :exec g:Lf_py "ghqExplManager.accept()"<CR>
    nnoremap <buffer> <silent> q             :exec g:Lf_py "ghqExplManager.quit()"<CR>
    nnoremap <buffer> <silent> i             :exec g:Lf_py "ghqExplManager.input()"<CR>
    nnoremap <buffer> <silent> <F1>          :exec g:Lf_py "ghqExplManager.toggleHelp()"<CR>

    if has_key(g:Lf_NormalMap, "Ghq")
        for i in g:Lf_NormalMap["Ghq"]
            exec 'nnoremap <buffer> <silent> '.i[0].' '.i[1]
        endfor
    endif
endfunction


function! leaderf#Ghq#managerId()
    " pyxeval() has bug
    if g:Lf_PythonVersion == 2
        return pyeval("id(ghqExplManager)")
    else
        return py3eval("id(ghqExplManager)")
    endif
endfunction
