pub mod command;
pub mod word;
pub mod list;

#[derive(Debug)]
pub struct RuleIf<'a> {
    condition: list::List<'a>,
    body: list::List<'a>,

    _else: list::List<'a>,
}

pub struct ElseClause