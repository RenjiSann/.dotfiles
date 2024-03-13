use log::warn;
use threadpool::ThreadPool;

use std::path::Path;
use std::{fs, io};

use crate::{utils::check_or_write_file, browser};

pub(crate) struct MonolithicQueueBrowser;

impl browser::Browser for MonolithicQueueBrowser {
    fn _browse(&self, root: &Path, path: &Path) -> anyhow::Result<()> {
        // Assume dir is valid

        // We create twice as many threads as we have cores.
        // Anyway, the tasks will be IO bound.
        let mut pool = ThreadPool::new(num_cpus::get() * 2);

        recurse_directories(path, &mut pool)?;

        pool.join();

        Ok(())
    }
}

fn recurse_directories(dir: &Path, pool: &mut ThreadPool) -> io::Result<()> {
    let p = dir.to_path_buf();
    pool.execute(move || match check_or_write_file(&p) {
        Err(_) => warn!(""),
        _ => (),
    });

    // Recurse in other dirs
    for entry in fs::read_dir(dir)? {
        let path = entry?.path();

        if path.is_dir() && !path.is_symlink() {
            recurse_directories(&path, pool)?;
        }
    }

    Ok(())
}
