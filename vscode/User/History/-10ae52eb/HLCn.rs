pub mod command;
pub mod word;
pub mod list;

use list::List;

#[derive(Debug, PartialEq, Eq)]
pub struct RuleIf<'a> {
    pub condition: List<'a>,
    pub body: List<'a>,
    pub elifs: Vec<RuleElif<'a>>,
    pub else_body: List<'a>,
}

impl<'a> RuleIf<'a> {
    pub fn new(condition: List<'a>, body: List<'a>) -> Self {

    }
}

#[derive(Debug, PartialEq, Eq)]
pub struct RuleElif<'a> {
    pub condition: List<'a>,
    pub body: List<'a>,
}