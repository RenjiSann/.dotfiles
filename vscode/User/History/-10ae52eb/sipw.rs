pub mod ast;

use ast::list::List;

#[derive(Debug, PartialEq, Eq)]
pub struct RuleIf<'a> {
    condition: List<'a>,
    body: List<'a>,
    elifs: Vec<RuleElif<'a>>,
    else_body: List<'a>,
}

impl<'a> RuleIf<'a> {
    pub fn new(
        condition: List<'a>,
        body: List<'a>,
        elifs: Vec<RuleElif<'a>>,
        else_body: List<'a>,
    ) -> Self {
        Self {
            condition,
            body,
            elifs,
            else_body,
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
pub struct RuleElif<'a> {
    condition: List<'a>,
    body: List<'a>,
}
