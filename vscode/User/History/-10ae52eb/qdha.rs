/// A
pub enum Token<'a> {
    If,
    Then,
    Else,
    Fi,
    SemiColumn,
    Word(&'a str),
}