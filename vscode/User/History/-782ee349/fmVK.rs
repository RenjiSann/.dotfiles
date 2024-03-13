use nom::{
    bytes::complete::tag,
    character::complete::{space0, space1},
    combinator::{map, opt},
    multi::many0,
    sequence::{delimited, pair, preceded, terminated},
    IResult, Parser,
};
use r42sh_ast::ast::{flow::rule_if::RuleIf, list::List};

use crate::parse_list;

/// Parse a rule with the if command
pub(crate) fn parse_rule_if<'a>(input: &'a str) -> IResult<&str, RuleIf<'a>> {
    let parser = delimited(
        terminated(tag("if"), space1),
        pair(
            terminated(
                parse_list, // If Condition
                pair(space0, tag("then")),
            ),
            pair(
                parse_list, // If body
                pair(
                    many0(
                        preceded(space0, parse_rule_elsif), // Elsifs
                    ),
                    opt(
                        parse_rule_else, // Else body
                    ),
                ),
            ),
        ),
        preceded(space0, tag("fi")),
    );
    parser
        .map(|(cond, (body, (elifs, else_bdy)))| {
            RuleIf::new(cond, body, elifs, else_bdy)
        })
        .parse(input)
}

#[allow(unused)]
fn parse_rule_elsif<'a>(
    input: &'a str,
) -> IResult<&'a str, (List<'a>, List<'a>)> {
    let mut parser = preceded(
        terminated(tag("elsif"), space1),
        pair(
            terminated(parse_list, pair(space0, tag("then"))),
            parse_list,
        ),
    );
    parser(input)
}

#[allow(unused)]
fn parse_rule_else<'a>(input: &'a str) -> IResult<&'a str, List<'a>> {
    let mut parser = preceded(pair(space0, tag("else")), parse_list);
    parser(input)
}

#[cfg(test)]
mod tests {
    use super::parse_rule_if;

    #[test]
    fn space_1() {
        let cmd = "if true ; then false ; fi";
        let res = parse_rule_if(cmd);
        if let Err(e) = &res {
            println!("{}", e.to_string());
        }
        debug_assert!(matches!(res, Ok(_)))
    }

    #[test]
    fn no_space() {
        let cmd = "if true ;then false ;fi";
        let res = parse_rule_if(cmd);
        if let Err(e) = &res {
            println!("{}", e.to_string());
        }
        debug_assert!(matches!(res, Ok(_)))
    }

    #[test]
    fn long_condition() {
        let cmd = "if true or dead go ;then false ;fi";
        let res = parse_rule_if(cmd);
        if let Err(e) = &res {
            println!("{}", e.to_string());
        }
        debug_assert!(matches!(res, Ok(_)))
    }

    #[test]
    fn long_body() {
        let cmd = "if true ;then false and alive stay ;fi";
        let res = parse_rule_if(cmd);
        if let Err(e) = &res {
            println!("{}", e.to_string());
        }
        debug_assert!(matches!(res, Ok(_)))
    }

    #[test]
    fn several_commands_condition() {
        let cmd = "if true ;false ; none;then false and alive stay ;fi";
        let res = parse_rule_if(cmd);
        if let Err(e) = &res {
            println!("{}", e.to_string());
        }
        debug_assert!(matches!(res, Ok(_)))
    }

    #[test]
    fn several_commands_body() {
        let cmd = "if true ;false ; none;then false and alive stay ;fi";
        let res = parse_rule_if(cmd);
        if let Err(e) = &res {
            println!("{}", e.to_string());
        }
        debug_assert!(matches!(res, Ok(_)))
    }

    mod else_clause {
        use crate::rule_if::parse_rule_if;

        #[test]
        fn simple_else() {
            let cmd = "if true ;then false ; else goto bed ;fi";
            let res = parse_rule_if(cmd);
            if let Err(e) = &res {
                println!("{}", e.to_string());
            }
            debug_assert!(matches!(res, Ok(_)))
        }

        #[test]
        fn else_touch_semi_col() {
            let cmd = "if true ;then false ;else goto bed ;fi";
            let res = parse_rule_if(cmd);
            if let Err(e) = &res {
                println!("{}", e.to_string());
            }
            debug_assert!(matches!(res, Ok(_)))
        }
    }

    mod elsif_clause {
        use crate::rule_if::parse_rule_if;

        #[test]
        fn elsif_1() {
            let cmd = "if true ;then false ;elsif false; then goto bed ;fi";
            let res = parse_rule_if(cmd);
            if let Err(e) = &res {
                println!("{}", e.to_string());
            }
            debug_assert!(matches!(res, Ok(_)))
        }

        #[test]
        fn elsif_2() {
            let cmd =
                "if true ;then false ; elsif I am false; then goto bed ;fi";
            let res = parse_rule_if(cmd);
            if let Err(e) = &res {
                println!("{}", e.to_string());
            }
            debug_assert!(matches!(res, Ok(_)))
        }

        #[test]
        fn elsif_several() {
            let cmd = "if true ;then false ; elsif I am false ; then goto bed ; elsif alive ; then set dead ;fi";
            let res = parse_rule_if(cmd);
            if let Err(e) = &res {
                println!("{}", e.to_string());
            }
            debug_assert!(matches!(res, Ok(_)))
        }

        #[test]
        fn elsif_then_else() {
            let cmd = "if true ;then false ; elsif I am false ; then goto bed ; else alive is dead ;fi";
            let res = parse_rule_if(cmd);
            if let Err(e) = &res {
                println!("{}", e.to_string());
            }
            debug_assert!(matches!(res, Ok(_)))
        }
    }

    mod errors {
        use crate::rule_if::parse_rule_if;

        #[test]
        fn if_missing_condition() {
            let cmd = "if ;then false ; fi";
            let res = parse_rule_if(cmd);
            debug_assert!(matches!(res, Err(_)))
        }
    }
}
