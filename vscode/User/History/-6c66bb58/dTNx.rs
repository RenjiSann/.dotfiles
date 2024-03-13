use lexpr::{self, Value};
use std::{collections::HashMap, fmt::Display};

type HMap = HashMap<String, ExprResult>;

trait Expr {
    fn eval_impl(&self, vars: &mut HMap) -> ExprResult;
    fn eval(&self) -> ExprResult {
        let mut vars = HMap::new();
        self.eval_impl(&mut vars)
    }
    fn dump(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
}

#[derive(Debug, PartialEq, Eq, Clone)]
enum ExprResult {
    Bool(bool),
    Int(i32),
}

impl ExprResult {
    pub fn unwrap_int(&self) -> i32 {
        match self {
            ExprResult::Bool(b) => panic!("Expected integer, got bool `{b}`"),
            ExprResult::Int(i) => *i,
        }
    }

    pub fn unwrap_bool(&self) -> bool {
        match self {
            ExprResult::Bool(b) => *b,
            ExprResult::Int(i) => panic!("Expected integer, got int `{i}`"),
        }
    }
}

impl From<i32> for ExprResult {
    fn from(value: i32) -> Self {
        ExprResult::Int(value)
    }
}

impl From<bool> for ExprResult {
    fn from(value: bool) -> Self {
        ExprResult::Bool(value)
    }
}

struct IntLiteral(i32);

impl Expr for IntLiteral {
    fn eval_impl(&self, _vars: &mut HMap) -> ExprResult {
        self.0.into()
    }

    fn dump(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

struct BoolLiteral(bool);

impl Expr for BoolLiteral {
    fn eval_impl(&self, _vars: &mut HMap) -> ExprResult {
        self.0.into()
    }

    fn dump(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

#[allow(dead_code)]
#[derive(Debug)]
enum Operator {
    Plus,
    Minus,
    Divide,
    Multiply,
    And,
    Or,
    Equal,
}
impl Display for Operator {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}",
            match self {
                Operator::Plus => "+",
                Operator::Minus => "-",
                Operator::Divide => "/",
                Operator::Multiply => "*",
                Operator::And => "and",
                Operator::Or => "or",
                Operator::Equal => "eq",
            }
        )
    }
}

struct BinOpExpr {
    left: Box<dyn Expr>,
    op: Operator,
    right: Box<dyn Expr>,
}

impl Expr for BinOpExpr {
    fn eval_impl(&self, vars: &mut HMap) -> ExprResult {
        use ExprResult::*;
        match self.op {
            Operator::Plus => Int(self.left.eval_impl(vars).unwrap_int()
                + self.right.eval_impl(vars).unwrap_int()),
            Operator::Minus => Int(self.left.eval_impl(vars).unwrap_int()
                - self.right.eval_impl(vars).unwrap_int()),
            Operator::Divide => Int(self.left.eval_impl(vars).unwrap_int()
                / self.right.eval_impl(vars).unwrap_int()),
            Operator::Multiply => Int(self.left.eval_impl(vars).unwrap_int()
                * self.right.eval_impl(vars).unwrap_int()),
            Operator::And => Bool(
                self.left.eval_impl(vars).unwrap_bool()
                    && self.right.eval_impl(vars).unwrap_bool(),
            ),
            Operator::Or => Bool(
                self.left.eval_impl(vars).unwrap_bool()
                    || self.right.eval_impl(vars).unwrap_bool(),
            ),
            Operator::Equal => Bool(
                match (self.left.eval_impl(vars), self.right.eval_impl(vars)) {
                    (Int(l), Int(r)) => r == l,
                    (Bool(l), Bool(r)) => r == l,
                    _ => {
                        panic!("Cannot check equality between bool and int")
                    }
                },
            ),
        }
    }

    fn dump(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "({} ", self.op)?;
        self.left.dump(f)?;
        write!(f, " ")?;
        self.right.dump(f)?;
        write!(f, ")")
    }
}

struct IfExpr {
    cond: Box<dyn Expr>,
    true_branch: Box<dyn Expr>,
    false_branch: Box<dyn Expr>,
}

impl Expr for IfExpr {
    fn eval_impl(&self, vars: &mut HMap) -> ExprResult {
        if self.cond.eval_impl(vars).unwrap_bool() {
            self.true_branch.eval_impl(vars)
        } else {
            self.false_branch.eval_impl(vars)
        }
    }

    fn dump(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "(if ")?;
        self.cond.dump(f);
        write!(f, " ")?;
        self.true_branch.dump(f);
        write!(f, " ")?;
        self.false_branch.dump(f);
        write!(f, ")")
    }
}

struct LetExpr {
    vname: String,
    vval: Box<dyn Expr>,
    body: Box<dyn Expr>,
}

impl Expr for LetExpr {
    fn eval_impl(&self, vars: &mut HMap) -> ExprResult {
        let val = self.vval.eval_impl(vars);
        vars.insert(self.vname.clone(), val);
        let res = self.body.eval_impl(vars);
        vars.remove(&self.vname);
        res
    }
}

struct RefExpr(String);

impl Expr for RefExpr {
    fn eval_impl(&self, vars: &mut HMap) -> ExprResult {
        match vars.get(&self.0) {
            Some(val) => val.clone(),
            None => panic!("Unkown variable `{}`", self.0),
        }
    }
}

fn parse(value: &Value) -> Box<dyn Expr> {
    use Operator::*;
    match value {
        Value::Cons(_) => match &value[0] {
            Value::Symbol(name) if name.as_ref() == "let" => {
                Box::new(LetExpr {
                    vname: value[1].to_string(),
                    vval: parse(&value[2]),
                    body: parse(&value[3]),
                })
            }
            Value::Symbol(name) if name.as_ref() == "if" => Box::new(IfExpr {
                cond: parse(&value[1]),
                true_branch: parse(&value[2]),
                false_branch: parse(&value[3]),
            }),
            Value::Symbol(s) => {
                let op = match s.as_ref() {
                    "+" => Plus,
                    "-" => Minus,
                    "/" => Divide,
                    "*" => Multiply,
                    "and" => And,
                    "or" => Or,
                    "eq" => Equal,
                    s => panic!("Unknown symbol `{s}`"),
                };
                Box::new(BinOpExpr {
                    left: parse(&value[1]),
                    op: op,
                    right: parse(&value[2]),
                })
            }
            default => panic!("Unexpected token `{default:?}`"),
        },
        Value::Number(nb) => {
            Box::new(IntLiteral(nb.as_i64().expect("Unhandled number") as i32))
        }
        Value::Symbol(s) if s.as_ref() == "true" => Box::new(BoolLiteral(true)),
        Value::Symbol(s) if s.as_ref() == "false" => {
            Box::new(BoolLiteral(false))
        }
        Value::Symbol(s) => {
            // Symbols different than 'true' or 'false' are considered
            // references
            println!("{s} handled as a reference");
            Box::new(RefExpr(s.to_string()))
        }
        default => panic!("Loul {default:?}"),
    }
}

///
struct PrintExpr(Box<dyn Expr>);

impl Expr for PrintExpr {
    fn eval_impl(&self, vars: &mut HMap) -> ExprResult {
        let res = self.0.eval_impl(vars);
        println!("Result: {:?}", res);
        res
    }
}

#[cfg(test)]
mod tests {

    mod evaluator {

        use crate::ex5::{
            BinOpExpr, BoolLiteral, Expr, ExprResult::*, IfExpr, IntLiteral,
            LetExpr, Operator::*, RefExpr,
        };

        #[test]
        fn test_add() {
            let expr = Box::new(BinOpExpr {
                left: Box::new(IntLiteral(5)),
                op: Plus,
                right: Box::new(IntLiteral(3)),
            });
            assert_eq!(expr.eval(), Int(8));
        }

        #[test]
        fn test_sub() {
            let expr = BinOpExpr {
                left: Box::new(IntLiteral(5)),
                op: Minus,
                right: Box::new(IntLiteral(7)),
            };
            assert_eq!(expr.eval(), Int(-2));
        }

        #[test]
        fn test_mal() {
            let expr = BinOpExpr {
                left: Box::new(IntLiteral(-9)),
                op: Multiply,
                right: Box::new(IntLiteral(7)),
            };
            assert_eq!(expr.eval(), Int(-63));
        }

        #[test]
        fn test_div() {
            let expr = BinOpExpr {
                left: Box::new(IntLiteral(13)),
                op: Divide,
                right: Box::new(IntLiteral(2)),
            };
            assert_eq!(expr.eval(), Int(6));
        }

        #[test]
        fn test_if() {
            let expr = IfExpr {
                cond: Box::new(BinOpExpr {
                    left: Box::new(IntLiteral(4)),
                    op: Equal,
                    right: Box::new(BinOpExpr {
                        left: Box::new(IntLiteral(3)),
                        op: Plus,
                        right: Box::new(IntLiteral(1)),
                    }),
                }),
                true_branch: Box::new(IntLiteral(5)),
                false_branch: Box::new(IntLiteral(8)),
            };
            assert_eq!(expr.eval(), Int(5));
        }

        #[test]
        fn test_bool_literal() {
            let expr = IfExpr {
                cond: Box::new(BoolLiteral(false)),
                true_branch: Box::new(IntLiteral(5)),
                false_branch: Box::new(IntLiteral(8)),
            };
            assert_eq!(expr.eval(), Int(8));
        }

        #[test]
        fn test_let_ref() {
            let expr = LetExpr {
                vname: "VOTAI".to_string(),
                vval: Box::new(IntLiteral(5)),
                body: Box::new(RefExpr("VOTAI".to_string())),
            };
            assert_eq!(expr.eval(), Int(5));
        }
    }

    mod parsing {
        use super::super::{parse, ExprResult::*};
        #[test]
        fn test_parse_1() {
            let values =
                lexpr::from_str("(let a 12 (+ a (if true 15 18)))").unwrap();
            let expr = parse(&values);
            assert_eq!(expr.eval(), Int(27));
        }

        #[test]
        fn test_parse_2() {
            let values = lexpr::from_str("(+ (* 12 14) (/ 4 2))").unwrap();
            let expr = parse(&values);
            assert_eq!(expr.eval(), Int(170));
        }

        #[test]
        fn test_parse_lazy_and() {
            let values =
                lexpr::from_str("(if (and (eq 12 14) (/ 1 0)) 13 15)").unwrap();
            let expr = parse(&values);
            assert_eq!(expr.eval(), Int(15));
        }

        #[test]
        fn test_parse_lazy_or() {
            let values =
                lexpr::from_str("(if (or (eq 14 14) (/ 1 0)) 13 15)").unwrap();
            let expr = parse(&values);
            assert_eq!(expr.eval(), Int(13));
        }
    }

    mod print_expr {
        use crate::ex5::{BoolLiteral, Expr, IfExpr, IntLiteral, PrintExpr};

        #[test]
        fn test_print_expr_1() {
            let expr = Box::new(IfExpr {
                cond: Box::new(BoolLiteral(false)),
                true_branch: Box::new(IntLiteral(5)),
                false_branch: Box::new(IntLiteral(8)),
            });
            let eval_res = expr.eval();
            let print_expr = PrintExpr(expr);
            assert_eq!(print_expr.eval(), eval_res);
        }
    }
}
