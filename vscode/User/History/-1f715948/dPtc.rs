
use crate::ast::list::List;

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
        elifs: Vec<(List<'a>, List<'a>)>,
        else_body: List<'a>,
    ) -> Self {
        let elifs = elifs.iter().map(|(cond, body)| RuleElif::(self))
        Self {
            condition,
            body,
            elifs,
            else_body,
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
struct RuleElif<'a> {
    condition: List<'a>,
    body: List<'a>,
}

impl<'a> From<(List<'a>, List<'a>)> for RuleElif<'a> {
    fn from(value: (List<'a>, List<'a>)) -> Self {
        Self{condition: value.0, body value.1}
    }
}