use anyhow::{anyhow, Result};
use clap::{Parser, ValueEnum};
use simple_logger::SimpleLogger;

use core::fmt;
use std::path::{PathBuf, self};

mod browser;
mod distributed;
mod monolithic;
mod monolithic_queue;
mod utils;

use browser::Browser;
use distributed::{DistributedBrowser, DistributedEnsurer};
use monolithic::MonolithicBrowser;
use monolithic_queue::MonolithicQueueBrowser;

#[derive(Debug, Copy, Clone, ValueEnum)]
enum Mode {
    Monolithic,
    MonolithicQueue,
    DistributedBrowser,
    DistributedEnsurer,
}

impl fmt::Display for Mode {
    fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {
        use Mode::*;
        match self {
            Monolithic => write!(fmt, "monolithic"),
            MonolithicQueue => write!(fmt, "monolithic-queue"),
            DistributedBrowser => write!(fmt, "distributed-browser"),
            DistributedEnsurer => write!(fmt, "distributed-ensurer"),
        }
    }
}

#[derive(Debug, Parser)]
#[command(author = "Dorian Péron", version = "0.1")]
struct CliArgs {
    #[arg(long, help = "required")]
    target_dir: String,

    #[arg(long)]
    mode: Mode,

    #[arg(long, default_value = "0")]
    rebrowse_interval: u64,

    #[arg(long)]
    debug: bool,

    #[arg(long)]
    broker_url: Option<String>,
}

fn browsing_mode(root: &Path) -> Result<()> {
    // Ensure target_dir is present
    let browser: Box<dyn Browser> = match args.mode {
        Mode::Monolithic => Box::new(MonolithicBrowser),
        Mode::MonolithicQueue => Box::new(MonolithicQueueBrowser),
        Mode::DistributedBrowser => Box::new(DistributedBrowser::new(
            args.broker_url.as_ref().unwrap(),
        )?),
        _ => panic!("unreachable"),
    };

    if args.rebrowse_interval == 0 {
        browser.browse_once(&root);
    } else {
        browser.browse_loop(&root, args.rebrowse_interval);
    }

    Ok(())
}

fn main() -> Result<()> {
    if std::env::var("RUST_LOG").is_err() {
        std::env::set_var("RUST_LOG", "info");
    }

    SimpleLogger::new().init().unwrap();

    let args = CliArgs::parse();

    match args.mode {
        Mode::DistributedBrowser | Mode::DistributedEnsurer => {
            if args.broker_url.is_none() {
                return Err(anyhow!("Missing --broker-url parameter"));
            }
        }
        _ => {
            if args.broker_url.is_some() {
                return Err(anyhow!("Unexpected --broker-url parameter"));
            }
        }
    }

    // Check dir
    let root = PathBuf::from(args.target_dir);
    if !root.exists() {
        return Err(anyhow!(
            "Invalid target directory: No such file or directory"
        ));
    }
    if !root.is_dir() {
        return Err(anyhow!("Invalid target directory: Not a directory"));
    }

    match args.mode {
        Mode::DistributedEnsurer => {
            let ensurer =
                DistributedEnsurer::new(args.broker_url.as_ref().unwrap())?;
            ensurer.run(&root)
        }
        _ => browsing_mode(&args),
    }
}
