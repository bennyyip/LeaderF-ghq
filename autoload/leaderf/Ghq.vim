if leaderf#versionCheck() == 0
    finish
endif

exec g:Lf_py "import vim, sys, os.path"
exec g:Lf_py "cwd = vim.eval('expand(\"<sfile>:p:h\")')"
exec g:Lf_py "sys.path.insert(0, os.path.join(cwd, 'python'))"
exec g:Lf_py "from ghqExpl import *"

function! leaderf#Ghq#Maps()
    nmapclear <buffer>
    nnoremap <buffer> <silent> <F1>          :exec g:Lf_py "ghqExplManager.toggleHelp()"<CR>
    nnoremap <buffer> <silent> <F5>          :exec g:Lf_py "ghqExplManager.refresh()"<CR>
    nnoremap <buffer> <silent> o             :exec g:Lf_py "ghqExplManager.accept()"<CR>
    nnoremap <buffer> <silent> <2-LeftMouse> :exec g:Lf_py "ghqExplManager.accept()"<CR>
    nnoremap <buffer> <silent> q             :exec g:Lf_py "ghqExplManager.quit()"<CR>
    nnoremap <buffer> <silent> i             :exec g:Lf_py "ghqExplManager.input()"<CR>
endfunction

function! leaderf#Ghq#startExpl(win_pos, ...)
    call leaderf#LfPy("ghqExplManager.startExplorer('".a:win_pos."')")
endfunction

