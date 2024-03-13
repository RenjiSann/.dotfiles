use r42sh_ast::command::Command;
use r42sh_parser::Parser;

use std::{fs::read_to_string, process::exit, error::Error};

use clap::Parser as ClapParser;

#[derive(ClapParser, Debug)]
#[group(required = true)]
struct Args {
    #[arg(short = 'c')]
    #[clap(group = "input")]
    /// Directly execute a shell command.
    command: Option<String>,

    #[clap(group = "input")]
    /// Provide the shell with the path to a file.
    filepath: Option<String>,
}

fn main() {
    let args = Args::parse();
    let input = match (args.command, args.filepath) {
        (Some(cmd), None) => cmd,
        (None, Some(filepath)) => match read_to_string(&filepath) {
            Ok(s) => s,
            Err(e) => {
                println!("{}: {}", filepath, e.to_string());
                exit(1)
            }
        },
        (_, _) => panic!("Impossible"),
    };
    println!("{:?}", Parser::parse(&input));
}
