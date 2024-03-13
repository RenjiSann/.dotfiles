use r42sh_ast::command::Command;
use r42sh_parser::Parser;

use clap::Parser as ClapParser;

#[derive(ClapParser, Debug)]
struct Args {
    #[arg(short='c')]
    #[group(id=1)]
    /// Trololol
    command: Option<String>
}

fn main() {
    let args = Args::parse();
    println!("Hello, world!");
}
