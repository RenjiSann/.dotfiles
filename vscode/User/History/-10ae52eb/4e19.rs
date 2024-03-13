pub mod command;
pub mod word;
pub mod list;

#[derive(Debug)]
struct RuleIf {
    condition: list::List
}