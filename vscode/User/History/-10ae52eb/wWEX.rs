pub mod command;
pub mod word;
pub mod list;

#[derive(Debug)]
pub struct RuleIf<'a> {
    pub condition: list::List<'a>,
    pub body: list::List<'a>,
    pub elifs: Vec<RuleElif<'a>>,
    pub else_body: list::List<'a>,
}

#[derive(Debug)]
pub struct RuleElif<'a> {
    pub condition: list::List<'a>,
    pub body: list::List<'a>,
}