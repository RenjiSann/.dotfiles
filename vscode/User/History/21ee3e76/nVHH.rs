use r42sh_ast::command::Command;
use r42sh_parser::Parser;

use std::fs::read_to_string;

use clap::Parser as ClapParser;

#[derive(ClapParser, Debug)]
struct Args {

    #[arg(short='c')]
    #[clap(group="input")]
    /// Directly execute a shell command.
    command: Option<String>,

    #[clap(group="input")]
    /// Provide the shell with the path to a file.
    filepath: Option<String>

}

fn main() {
    let args = Args::parse();
    let input = match (args.command, args.filepath) {
        (Some(cmd), None) => Ok(cmd),
        None => read_to_string(args.filepath.unwrap())
    };
    println!("Hello, world!");
}