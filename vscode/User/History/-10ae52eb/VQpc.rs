/// A
enum Token<'a> {
    If,
    Then,
    Else,
    Fi,
    Word(&'a str),
}