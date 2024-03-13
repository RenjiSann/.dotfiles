-- Override Cosmic editor options

local g = vim.g
local map = require("cosmic.utils").map
local opt = vim.opt

-- Default leader is <space>
-- g.mapleader = ','

-- Default indent = 2
opt.shiftwidth = 4
opt.softtabstop = 4
opt.tabstop = 4
opt.wrap = true

-- Add additional keymaps or disable existing ones
-- To view maps set, use `:Telescope keymaps`
-- or `:map`, `:map <leader>`

-- Example: Additional insert mapping:
-- map('i', 'jj', '<esc>')

-- Mapping options:
-- map('n', '<leader>gg', ':LazyGit<CR>')

-- Example: Disable find files keymap
-- vim.keymap.del('n', '<leader>f')

-- See :h vim.keymap for more info

-- Disable search highlight
map("n", "<leader>h", ":noh<CR>", { desc = "De-highlight search matches" })
