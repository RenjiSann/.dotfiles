-- overriding default plugin configs!

local M = {}

M.mason = {
  ensure_installed = {
    -- lua stuff
    "lua-language-server",

    -- rust
    "rust-analyzer"
  },
}

M.treesitter = {
  ensure_installed = {
    "vim",
--  "html",
--  "css",
--  "javascript",
    "json",
    "toml",
    "markdown",
    "c",
    "bash",
    "lua",
    "rust",
--  "norg",
  },
}

M.nvimtree = {
  git = {
    enable = true,
    ignore = false
  },

  renderer = {
    highlight_git = true,
    icons = {
      show = {
        git = true,
      },
    },
  },

  filters = {
    dotfiles = true,
  }
}

M.blankline = {
  filetype_exclude = {
    "help",
    "terminal",
    "alpha",
    "packer",
    "lspinfo",
    "TelescopePrompt",
    "TelescopeResults",
    "nvchad_cheatsheet",
    "lsp-installer",
    "norg",
    "",
  },
}

M.alpha = {
  header = {
    val = {
      "           ▄ ▄                   ",
      "       ▄   ▄▄▄     ▄ ▄▄▄ ▄ ▄     ",
      "       █ ▄ █▄█ ▄▄▄ █ █▄█ █ █     ",
      "    ▄▄ █▄█▄▄▄█ █▄█▄█▄▄█▄▄█ █     ",
      "  ▄ █▄▄█ ▄ ▄▄ ▄█ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄  ",
      "  █▄▄▄▄ ▄▄▄ █ ▄ ▄▄▄ ▄ ▄▄▄ ▄ ▄ █ ▄ ",
      "▄ █ █▄█ █▄█ █ █ █▄█ █ █▄█ ▄▄▄ █ █ ",
      "█▄█ ▄ █▄▄█▄▄█ █ ▄▄█ █ ▄ █ █▄█▄█ █ ",
      "    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█ █▄█▄▄▄█     ",
    },
  },
}


return M
