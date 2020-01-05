# LeaderF-ghq

This Plugin use LeaderF to navigate to a repository managed by [ghq](https://github.com/motemen/ghq).

# Usage
```
:LeaderfGhq
```
Press `F1` to get more help


```vim
" Set commands to be executed when accept selection
let g:Lf_GhqAcceptSelectionCmd = 'tabe | Vaffle'

" mappings
nnoremap <silent> <Space>fq :<C-u>Leaderf ghq --popup<CR>
```

# LICENSE
MIT
