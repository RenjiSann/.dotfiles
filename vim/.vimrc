"	RenjiSann .vimrc 2021
" Start



"	PLUGINS
call plug#begin('~/.config/nvim/plugged')

"Status lines
Plug 'vim-airline/vim-airline'
"Plug 'rbong/vim-crystalline'

"	Linters
Plug 'neoclide/coc.nvim', {'branch': 'release'}
"Plug 'dense-analysis/ale'


Plug 'airblade/vim-gitgutter'
Plug 'townk/vim-autoclose'
Plug 'sheerun/vim-polyglot'

"	Themes
Plug 'joshdick/onedark.vim'
"Plug 'humanoid-colors/vim-humanoid-colorscheme'

call plug#end()
"End Plugins




set showtabline=2
set guioptions-=e

set laststatus=2					"Change Statusline
set background=dark
colorscheme onedark					"Change colorTheme
set laststatus=2
set statusline=%!DetectMode(mode())


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

set eadirection="ver"
set termguicolors

"Map F7 to reindent all file
map <F7> gg=G<C-o><C-o>
syntax enable


" End
