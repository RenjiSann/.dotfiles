/// A
#[derive(Debug)]
pub enum Token<'a> {
    If,
    Then,
    Else,
    Fi,
    SemiColumn,
    LineFeed,
    SingleQuote,
    Word(&'a str),
}