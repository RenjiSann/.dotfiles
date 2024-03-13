use anyhow::Result;
use log::{warn, info};

use core::time;
use std::{path::Path, thread};

pub(crate) trait Browser {
    fn _browse(&self, root: &Path, path: &Path) -> Result<()>;

    fn browse_once(&self, path: &Path) {
        info!("Scanning file tree once");
        match self._browse(path) {
            Err(e) => warn!("Error: {}", e),
            _ => ()
        }
    }

    fn browse_loop(&self, path: &Path, interval: u64) {
        info!("Monitoring file tree with {}s interval", interval);
        let sleep_time = time::Duration::from_secs(interval);
        loop {
            match self._browse(path, path) {
                Err(e) => warn!("Error: {}", e),
                _ => ()
            }
            thread::sleep(sleep_time);
        }

    }
}
