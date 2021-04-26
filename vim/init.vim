"	RenjiSann .vimrc 2020
" Start



" PLUGINS
call plug#begin('~/.config/nvim/plugged')

"Status lines
"Plug 'vim-airline/vim-airline'
"Plug 'vim-airline/vim-airline-themes'
"Plug 'rbong/vim-crystalline'

Plug 'w0rp/ale'
Plug 'airblade/vim-gitgutter'
Plug 'townk/vim-autoclose'
Plug 'sheerun/vim-polyglot'
Plug 'leafgarland/typescript-vim'

" Themes
Plug 'joshdick/onedark.vim'

call plug#end()
"End Plugins

set showtabline=2
set guioptions-=e




set laststatus=2					"Change Statusline
set background=dark
colorscheme humanoid					"Change colorTheme

"Begin statuslin
set noshowmode
set noruler

" Get current filetype
function! CheckFT(filetype)
  if a:filetype == ''
    return '-'
  else
    return tolower(a:filetype)
  endif
endfunction

function! AleStatus() abort
  let l:counts = ale#statusline#Count(bufnr(''))

  let l:all_errors = l:counts.error + l:counts.style_error
  let l:all_non_errors = l:counts.total - l:all_errors

  return l:counts.total == 0 ? 'OK' : printf(
  \ '%dW %dE',
  \ all_non_errors,
  \ all_errors
  \)
endfunction

function! GitGutterStatus()
  let [a,m,r] = GitGutterGetHunkSummary()
  return printf('+%d ~%d -%d', a, m, r)
endfunction

" set colors for statusline based on mode
function! DetectMode(mode)
  if empty($DISPLAY)
    let left=""
    let right=""
  else
    let left=""
    let right=""
  end

  let statusline=""
  if a:mode == 'n'
    let statusline .= "%#ModeNFGCS#\ " . left
    let statusline .= "%#ModeNFGC#\ NORMAL\ "
    let statusline .= "%#ModeNFGCS#" . right . "\ " . left
    let statusline .= "%#ModeNFGC#%[%n\ ̷%{bufnr('$')}\ "
  elseif a:mode == 'i'
    let statusline .= "%#ModeIFGCS#\ " . left
    let statusline .= "%#ModeIFGC#\ INSERT\ "
    let statusline .= "%#ModeIFGCS#" . right . "\ " . left
    let statusline .= "%#ModeIFGC#%[%n\ ̷%{bufnr('$')}\ "
  elseif a:mode == 'R'
    let statusline .= "%#ModeRFGCS#\ " . left
    let statusline .= "%#ModeRFGC#\ REPLACE\ "
    let statusline .= "%#ModeRFGCS#" . right . "\ " . left
    let statusline .= "%#ModeRFGC#%[%n\ ̷%{bufnr('$')}\ "
  elseif a:mode ==# 'v'
    let statusline .= "%#ModeVFGCS#\ " . left
    let statusline .= "%#ModeVFGC#\ VISUAL\ "
    let statusline .= "%#ModeVFGCS#" . right . "\ " . left
    let statusline .= "%#ModeVFGC#%[%n\ ̷%{bufnr('$')}\ "
  elseif a:mode ==# 'V'
    let statusline .= "%#ModeVFGCS#\ " . left
    let statusline .= "%#ModeVFGC#\ VISUAL\ "
    let statusline .= "%#ModeVFGCS#" . right . "\ " . left
    let statusline .= "%#ModeVFGC#%[%n\ ̷%{bufnr('$')}\ "
  elseif a:mode ==# ''
    let statusline .= "%#ModeVFGCS#\ " . left
    let statusline .= "%#ModeVFGC#\ VISUAL\ "
    let statusline .= "%#ModeVFGCS#" . right . "\ " . left
    let statusline .= "%#ModeVFGC#%[%n\ ̷%{bufnr('$')}\ "
  elseif a:mode ==# 'c'
    let statusline=""
    let statusline .= "%#ModeCFGCS#\ " . left
    let statusline .= "%#ModeCFGC#\ COMMAND\ "
    let statusline .= "%#ModeCFGCS#" . right . "\ " . left
    let statusline .= "%#ModeCFGC#%[%n\ ̷%{bufnr('$')}\ "
  elseif a:mode ==# 't'
    let statusline .= "%#ModeTFGCS#\ " . left
    let statusline .= "%#ModeTFGC#\ TERMINAL\ "
    let statusline .= "%#ModeTFGCS#" . right . "\ " . left
    let statusline .= "%#ModeTFGC#%[%n\ ̷%{bufnr('$')}\ "
  elseif a:mode == 'v' || a:mode == 'V' || a:mode == '^V' || a:mode == 's' || a:mode == 'S' || a:mode == '^S'
    let statusline .= "%#ModeVFGCS#\ " . left
    let statusline .= "%#ModeVFGC#\ VISUAL\ "
    let statusline .= "%#ModeVFGCS#" . right . "\ " . left
    let statusline .= "%#ModeVFGC#%[%n\ ̷%{bufnr('$')}\ "
  endif
  if &mod == 1
	let statusline .= "%#Modified#\ %.20f\ ⁺%#ModifiedS#" . right . "\ "
  else
	let statusline .= "%#Buffer#\ %.20f\ %#BufferS#" . right . "\ "
  endif
  let statusline .= "%="
  if exists('*fugitive#statusline') || &rtp =~ 'GitGutter'
    if exists('*fugitive#statusline')
      let statusline .= "%#BufferS#" . left . "%#SLGreen#\ %{FugitiveHead()}\ "
    else
      let statusline .= "%#BufferS#" . left
    endif
    if &rtp =~ 'GitGutter'
      let statusline .= "%#SLBlue#\ %{GitGutterStatus()}\ %#BufferS#" . right . "\ "
    else
      let statusline .= "%#BufferS#" . right . "\ "
    endif
  endif
  let statusline .= "%#BufferS#" . left . "%#Buffer#\ %{CheckFT(&filetype)}\ "
  if &rtp =~ 'ale'
    if AleStatus() == "OK"
      let statusline .= "%#SLLimiter#│%#CursorStatus#\ %{AleStatus()}\ %#BufferS#" . right . "\ "
    else
      let statusline .= "\ %#BufferError#\ %{AleStatus()}\ %#BufferErrorS#" . right . "\ "
    endif
  else
    let statusline .= "%#BufferS#" . right . "\ "
  endif
  let statusline .= "%#BufferS#" . left . "%#ursorStatus#\ %-8.(%l,%c%)%#ModeNFGC#\ %P\ %#ModeNFGCS#" . right . "\ "
  return statusline
  return ' '
endfunction

set laststatus=2
set statusline=%!DetectMode(mode())

e
"End Status line

set nu						"Display lines number
set bs=2 					"Set Backspace mode to 2
set noexpandtab				"TAB inserts a tabulation instead of spaces
set hls ic					"searching highlight matching text and ignore case
set autoindent				"Auto indent new lines depending on the one above
set tabstop=4				"Make TAB length equal to 4 spaces
set softtabstop=4			"Set the number of tabs to clear when hitting backspace
set shiftwidth=4			"Set the indent shift width
set colorcolumn=80			"Set a color column at 80th

set termguicolors

syntax enable


" End
