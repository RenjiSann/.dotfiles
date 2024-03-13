use anyhow::anyhow;
use pathdiff;

use std::fs;
use std::path::Path;

use crate::{browser, utils::check_or_write_file};

pub(crate) struct MonolithicBrowser;

impl browser::Browser for MonolithicBrowser {
    fn _browse(&self, root: &Path, path: &Path) -> anyhow::Result<()> {
        let dir = root.join(path);
        // Assume dir is valid
        check_or_write_file(&dir)?;

        // Recurse in other dirs
        for entry in fs::read_dir(dir)? {
            let mut path = entry?.path();
            if path.is_dir() && !path.is_symlink() {
                path = match pathdiff::diff_paths(path, root) {
                    Some(p) => p,
                    None => return Err(anyhow!("Cannot do path diff")),
                };
                self._browse(root, &path)?;
            }
        }
        Ok(())
    }
}
