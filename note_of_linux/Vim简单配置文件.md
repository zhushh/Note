## Vim简单的配置文件

```shell
set nocompatible
set number
filetype plugin on
set history=1000
set smartindent
" set comment color
" selected in /usr/share/vim/vim74/colors
colorscheme desert
" tab width = 4
set tabstop=4
" 编辑模式按退格键时缩回的长度,使用expandtab时才有用
set softtabstop=4
" 每一级的缩进长度
set shiftwidth=4
" set expandtab
set expandtab
set autoindent
" set tab useful for [mM]akefile
autocmd BufNewFile,BufRead *[mM]akefile,*.mk,*.mak,*.dsp setf make
set showmatch
set ruler
set nohls
set incsearch
syntax on
set showcmd
""set scrolloff=15
set scrolloff=15

" autocomplete 
inoremap ( ()<ESC>i
inoremap ) <c-r>=ClosePair(')')<CR>
inoremap [ []<ESC>i
inoremap ] <c-r>=ClosePair(']')<CR>
inoremap { {<CR>}<ESC>i<Up><End><CR>
inoremap } <c-r>=ClosePair('}')<CR>
inoremap ' ''<ESC>i
inoremap " ""<ESC>i
function! ClosePair(char)
    if getline('.')[col('.') - 1] == a:char
		return "\<Right>"
	else
		return a:char
	endif
endfunction

" replace the tab with blanks
nmap tt :%s/\t/    /g<CR>

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""新文件标题
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"新建.c,.h,.sh,.java文件，自动插入文件头
autocmd BufNewFile *.cpp,*.[ch],*.sh,*.rb,*.java,*.py exec ":call SetTitle()"
""定义函数SetTitle，自动插入文件头
func SetTitle()
	"如果文件类型为.sh文件
	if &filetype == 'sh'
		call setline(1,"\#!/bin/bash")
		call append(line("."), "")
	elseif &filetype == 'python'
		call setline(1,"#!/usr/bin/env python")
		call append(line("."),"# coding=utf-8")
		call append(line(".")+1, "")
	elseif &filetype == 'ruby'
		call setline(1,"#!/usr/bin/env ruby")
		call append(line("."),"# encoding: utf-8")
		call append(line(".")+1, "")
	" elseif &filetype == 'mkd'
	" call setline(1,"<head><meta charset=\"UTF-8\"></head>")
	else
		call setline(1, "/*************************************************************************")
		call append(line("."), " > File Name: ".expand("%"))
		call append(line(".")+1, " > Author: zhushh")
		call append(line(".")+2, " > Mail: ")
		call append(line(".")+3, " > Created Time: ".strftime("%c"))
		call append(line(".")+4, " ************************************************************************/")
		call append(line(".")+5, "")
	endif
	if expand("%:e") == 'cpp'
		call append(line(".")+6, "#include <iostream>")
		call append(line(".")+7, "using namespace std;")
		call append(line(".")+8, "")
	endif
	if &filetype == 'c'
		call append(line(".")+6, "#include <stdio.h>")
			call append(line(".")+7, "")
	endif
	if expand("%:e") == 'h'
		call append(line(".")+6, "#ifndef _".toupper(expand("%:r"))."_H")
		call append(line(".")+7, "#define _".toupper(expand("%:r"))."_H")
		call append(line(".")+8, "#endif")
	endif
	if &filetype == 'java'
		call append(line(".")+6,"public class ".expand("%:r"))
		call append(line(".")+7,"")
	endif
	"新建文件后，自动定位到文件末尾
endfunc
autocmd BufNewFile * normal G

"map <F6> :call FormatSrc()<CR><CR>
"" code format start
"func FormatSrc()
"    exec "w"
"	if &filetype == 'c'
"		exec "!astyle --style=ansi -a --suffix=none %"
"	elseif &filetype == 'cpp' || &filetype == 'hpp'
"	    exec "r !astyle --style=ansi --one-line=keep-statements -a --suffix=none %> /dev/null 2>&1"
"	elseif &filetype == 'perl'
"		exec "!astyle --style=gnu --suffix=none %"
"	elseif &filetype == 'py'||&filetype == 'python'
"	    exec "r !autopep8 -i --aggressive %"
"	elseif &filetype == 'java'
"	    exec "!astyle --style=java --suffix=none %"
"	elseif &filetype == 'jsp'
"	    exec "!astyle --style=gnu --suffix=none %"
"	elseif &filetype == 'xml'
"	    exec "!astyle --style=gnu --suffix=none %"
"	else
"		exec "normal gg=G"
"		return
"	endif
"	exec "e! %"
"endfunc
"" end format function
```
