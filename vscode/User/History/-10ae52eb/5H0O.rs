pub mod command;
pub mod word;
pub mod list;

#[derive(Debug)]
struct RuleIf<'a> {
    condition: list::List<'a>
}