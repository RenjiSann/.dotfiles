/// A
pub enum Token<'a> {
    If,
    Then,
    Else,
    Fi,
    SemiColumn,
    LineFeed,
    Word(&'a str),
}