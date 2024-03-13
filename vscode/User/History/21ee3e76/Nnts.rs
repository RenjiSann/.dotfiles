use r42sh_ast::command::Command;
use r42sh_parser::Parser;

use clap::Parser as ClapParser;

#[derive(ClapParser, Debug)]
struct Args {

    #[arg(short='c')]
    #[clap(group="input")]
    /// Trololol
    command: Option<String>,

    #[clap(group="input")]
    /// Trololol
    filepath: Option<String>

}

fn main() {
    let args = Args::parse();
    println!("Hello, world!");
}
