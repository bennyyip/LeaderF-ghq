" Definition of 'arguments' can be similar as
" https://github.com/Yggdroot/LeaderF/blob/master/autoload/leaderf/Any.vim#L85-L140
let s:extension = {
            \   "name": "ghq",
            \   "help": "navigate ghq repos",
            \   "manager_id": "leaderf#Ghq#managerId",
            \   "arguments": [
            \   ]
            \ }

" In order that `Leaderf ghq` is available
call g:LfRegisterPythonExtension(s:extension.name, s:extension)

command! -bar -nargs=0 LeaderfGhq Leaderf ghq

" In order to be listed by :LeaderfSelf
call g:LfRegisterSelf("LeaderfGhq", "navigate ghq repos")
