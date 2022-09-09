local M = {}
local override = require "custom.override"

M.plugins = {

  override = {
    ["nvim-treesitter/nvim-treesitter"] = override.treesitter,
    ["lukas-reineke/indent-blankline.nvim"] = override.blankline,
    ["goolord/alpha-nvim"] = override.alpha,
    ["kyazdani42/nvim-tree.lua"] = override.nvimtree,
    ["williamboman/mason.nvim"] = override.mason,
  },

  user = require "custom.plugins",
}

M.ui = {
  theme = "onedark",
  theme_toggle = { "onedark", "one_light" },
}

M.mappings = require "custom.mappings"

return M
