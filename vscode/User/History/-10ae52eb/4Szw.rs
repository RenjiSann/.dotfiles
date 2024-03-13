pub mod command;
pub mod word;
pub mod list;

use list::List;

#[derive(Debug)]
pub struct RuleIf<'a> {
    pub condition: list::List<'a>,
    pub body: list::List<'a>,
    pub elifs: Vec<RuleElif<'a>>,
    pub else_body: list::List<'a>,
}

impl<'a> RuleIf<'a> {
    pub fn new(condition: List<'a>, body: List)
}

#[derive(Debug)]
pub struct RuleElif<'a> {
    pub condition: list::List<'a>,
    pub body: list::List<'a>,
}