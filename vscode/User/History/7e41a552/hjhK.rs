use error::ParseError;
use nom::{
    branch::alt,
    bytes::complete::tag,
    character::complete::{
        alpha1, alphanumeric1, char, multispace0, newline, space0, space1,
    },
    combinator::{eof, map, opt, recognize},
    multi::{many0, many1, separated_list0, separated_list1},
    sequence::{delimited, pair, preceded, terminated},
    IResult,
    error::ParseError
};
use r42sh_ast::ast::{command::Command, list::List, word::Word};

mod error;
mod rule_if;

pub(crate) const RESERVED_KEYWORDS: &[&str] = &[
    "if", "then", "elsif", "else", "fi", "while", "until", "for", "do", "done",
];

pub struct Parser;

impl Parser {
    pub fn parse<'a>(input: &'a str) -> IResult<&str, List<'_>> {
        alt((
            terminated(parse_list, alt((eof_into_null_byte, newline))),
            // Create empty vec to match type
            map(alt((eof_into_null_byte, newline)), |_| vec![].into()),
        ))(input)
    }
}

fn parse_word<'a>(input: &'a str) -> IResult<&'a str, Word<'a>> {
    let parser = pair(
        alt((alpha1, tag("_"))),
        many0(alt((alphanumeric1, tag("_")))),
    );
    map(recognize(parser), Word::from)(input)
}

fn parse_non_reserved_word<'a>(input: &'a str) -> IResult<&'a str, Word<'a>> {
    let res = parse_word(input);
    match res {
        Ok(x) if { RESERVED_KEYWORDS.contains(&x.1.text()) } => {
            Err(crate::ParseError::new(format!(
                "{} is a reserved word",
                x.1.text()
            )))
        }
        Ok(x) => Ok(x),
        Err(e) => Err(e),
    }
}

fn parse_simple_command<'a>(input: &'a str) -> IResult<&'a str, Command<'a>> {
    let parser = trim_spaces(pair(
        parse_non_reserved_word,
        preceded(space1, separated_list0(space1, parse_word)),
    ));
    map(parser, move |v| v.into())(input)
}

fn parse_command<'a>(input: &'a str) -> IResult<&'a str, Command<'a>> {
    parse_simple_command(input)
}

fn parse_list<'a>(input: &'a str) -> IResult<&'a str, List<'a>> {
    let parser = pair(
        // A command followed by potential spaces
        // COMMAND <blank>*
        terminated(parse_command, space0),
        // Then any number of repetition of semicolumn, maybe blanks,
        // and a command. It ends with possibly more blanks and a semicolumn
        // (; <blank>* COMMAND)* [<blank>* ;]
        terminated(
            many0(preceded(pair(char(';'), space0), parse_command)),
            opt(pair(space0, char(';'))),
        ),
    );

    map(parser, move |(first, rest)| {
        [first].into_iter().chain(rest).into()
    })(input)
}

pub(crate) fn trim_spaces<'a, P, O, E>(
    parser: P,
) -> impl FnMut(&'a str) -> IResult<&'a str, O, E>
where
    P: nom::Parser<&'a str, O, E>,
    E: ParseError<&'a str>,
{
    delimited(space0, parser, space0)
}

pub(crate) fn trim_spaces_newlines<'a, P, O, E>(
    parser: P,
) -> impl FnMut(&'a str) -> IResult<&'a str, O, E>
where
    P: nom::Parser<&'a str, O, E>,
    E: ParseError<&'a str>,
{
    delimited(multispace0, parser, multispace0)
}

fn eof_into_null_byte<'a>(input: &'a str) -> IResult<&str, char> {
    map(eof, |out| '\0')(input)
}

#[cfg(test)]
mod parser_tests {
    use crate::Parser;

    mod parse_word_tests {
        use crate::parse_word;

        #[test]
        pub fn word_simple() {
            assert_eq!(parse_word("input"), Ok(("", "input".into())));
        }

        #[test]
        pub fn word_start_underscore() {
            assert_eq!(parse_word("_input"), Ok(("", "_input".into())));
        }

        #[test]
        pub fn word_space() {
            assert_eq!(parse_word("in put"), Ok((" put", "in".into())));
        }

        #[test]
        pub fn word_end_digit() {
            assert_eq!(parse_word("number1"), Ok(("", "number1".into())));
        }

        #[test]
        pub fn word_start_digit() {
            assert!(matches!(parse_word("1number"), Err(_)));
        }
    }

    mod parse_simple_command_test {
        use crate::parse_simple_command;

        #[test]
        pub fn simple_command_simple() {
            assert_eq!(
                parse_simple_command("simple"),
                Ok(("", vec!["simple"].into()))
            );
        }

        #[test]
        pub fn simple_command_two_words() {
            assert_eq!(
                parse_simple_command("one two"),
                Ok(("", vec!["one", "two"].into()))
            );
        }

        #[test]
        pub fn simple_command_5_words() {
            assert_eq!(
                parse_simple_command("one two three four five"),
                Ok(("", vec!["one", "two", "three", "four", "five"].into()))
            );
        }

        #[test]
        pub fn simple_command_sep_tabs() {
            assert_eq!(
                parse_simple_command("one\ttwo"),
                Ok(("", vec!["one", "two"].into()))
            );
        }

        #[test]
        pub fn simple_command_two_spaces() {
            assert_eq!(
                parse_simple_command("one  two"),
                Ok(("", vec!["one", "two"].into()))
            );
        }

        #[test]
        pub fn simple_command_space_tab() {
            assert_eq!(
                parse_simple_command("one \ttwo"),
                Ok(("", vec!["one", "two"].into()))
            );
        }
    }

    #[test]
    pub fn parse_eof() {
        Parser::parse("");
    }
}
