use pathdiff;

use std::fs;
use std::path::Path;

use crate::{utils::check_or_write_file, browser};

pub(crate) struct MonolithicBrowser;

impl browser::Browser for MonolithicBrowser {
    fn _browse(&self, root: &Path, path: &Path) -> anyhow::Result<()> {
        let dir = root.join(path);
        // Assume dir is valid
        check_or_write_file(&dir)?;

        // Recurse in other dirs
        for entry in fs::read_dir(dir)? {

            let path = entry?.path();
            if path.is_dir() && !path.is_symlink() {

                self._browse(root, &path)?;
            }
        }
        Ok(())
    }
}
