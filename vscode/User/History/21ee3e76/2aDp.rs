use r42sh_ast::command::Command;
use r42sh_parser::Parser;

use clap::{self, Parser};

#[derive(Parser, Debug)]
struct Args {
    #[arg()]
    command: String
}

fn main() {
    let args = Args::parse();
    println!("Hello, world!");
}
