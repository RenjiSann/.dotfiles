use r42sh_ast::command::Command;
use r42sh_parser::Parser;

use clap::Parser as ClapParser;

#[derive(ClapParser, Debug)]
struct Args {

    #[arg(short='c')]
    #[clap(group="input")]
    /// Provide the shell with the path to a file.
    command: Option<String>,

    #[clap(group="input")]
    /// Directly execute a shell command.
    filepath: Option<String>

}

fn main() {
    let args = Args::parse();
    println!("Hello, world!");
}