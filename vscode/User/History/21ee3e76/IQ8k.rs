use r42sh_ast::command::Command;
use r42sh_parser::Parser;

use clap::Parser as ClapParser;

#[derive(ClapParser, Debug)]
struct Args {
    #[arg(short="-c")]
    command: String
}

fn main() {
    let args = Args::parse();
    println!("Hello, world!");
}
