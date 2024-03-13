use lexpr::{self, Parser, Value};
use std::collections::HashMap;

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

#[derive(Debug, PartialEq, Eq, Clone)]
enum ExprResult {
    Bool(bool),
    Int(i32),
}

#[derive(Debug)]
enum Expr {
    BinOp {
        l: Box<Expr>,
        op: Operator,
        r: Box<Expr>,
    },
    IfExpr {
        cond: Box<Expr>,
        true_branch: Box<Expr>,
        false_branch: Box<Expr>,
    },
    Literal(i32),
    LiteralBool(bool),
    Let {
        vname: String,
        vval: Box<Expr>,
        code: Box<Expr>,
    },
    Ref(String),
}

type HMap = HashMap<String, ExprResult>;

impl Expr {
    fn eval(&self) -> ExprResult {
        let mut hm: HMap = HashMap::new();
        self.eval_impl(&mut hm)
    }

    fn eval_to_int(&self, vars: &mut HMap) -> i32 {
        match self.eval_impl(vars) {
            ExprResult::Int(i) => i,
            _ => panic!("Expected number"),
        }
    }

    fn eval_to_bool(&self, vars: &mut HMap) -> bool {
        match self.eval_impl(vars) {
            ExprResult::Bool(b) => b,
            _ => panic!("Expected bool"),
        }
    }

    fn eval_impl(&self, vars: &mut HMap) -> ExprResult {
        match self {
            Expr::BinOp { l, op, r } => {
                use ExprResult::*;
                match op {
                    Operator::Plus => {
                        Int(l.eval_to_int(vars) + r.eval_to_int(vars))
                    }
                    Operator::Minus => {
                        Int(l.eval_to_int(vars) - r.eval_to_int(vars))
                    }
                    Operator::Divide => {
                        Int(l.eval_to_int(vars) / r.eval_to_int(vars))
                    }
                    Operator::Multiply => {
                        Int(l.eval_to_int(vars) * r.eval_to_int(vars))
                    }
                    Operator::And => {
                        Bool(l.eval_to_bool(vars) && r.eval_to_bool(vars))
                    }
                    Operator::Or => {
                        Bool(l.eval_to_bool(vars) || r.eval_to_bool(vars))
                    }
                    Operator::Equal => {
                        Bool(match (l.eval_impl(vars), r.eval_impl(vars)) {
                            (Int(l), Int(r)) => r == l,
                            (Bool(l), Bool(r)) => r == l,
                            _ => {
                                panic!("Cannot check equality between bool and int")
                            }
                        })
                    }
                }
            }
            Expr::IfExpr {
                cond,
                true_branch,
                false_branch,
            } => {
                use ExprResult::*;
                let cond = match cond.eval() {
                    Bool(b) => b,
                    Int(_) => panic!("condition needs a boolean"),
                };

                if cond {
                    true_branch.eval()
                } else {
                    false_branch.eval()
                }
            }
            Expr::Literal(x) => ExprResult::Int(*x),
            Expr::LiteralBool(b) => ExprResult::Bool(*b),
            Expr::Let { vname, vval, code } => {
                let val = vval.eval_impl(vars);
                vars.insert(vname.clone(), val);
                let res = code.eval_impl(vars);
                vars.remove(vname);
                res
            }
            Expr::Ref(vname) => match vars.get(vname) {
                Some(val) => val.clone(),
                None => panic!("Unkown variable"),
            },
        }
    }
}

fn parse(value: &Value) -> Expr {
    use Expr::*;
    use Operator::*;
    match value {
        Value::Cons(_) => match &value[0] {
            Value::Symbol(name) if name.as_ref() == "let" => Let {
                vname: value[1].to_string(),
                vval: Box::new(parse(&value[2])),
                code: Box::new(parse(&value[3])),
            },
            Value::Symbol(name) if name.as_ref() == "+" => BinOp {
                l: Box::new(parse(&value[1])),
                op: Plus,
                r: Box::new(parse(&value[2])),
            },
            Value::Symbol(name) if name.as_ref() == "if" => IfExpr {
                cond: (),
                true_branch: (),
                false_branch: (),
            },
            Value::Symbol(s) => todo!("Yeet: {s}"),
            Value::Nil => todo!(),
            Value::Null => todo!(),
            Value::Bool(_) => todo!(),
            Value::Number(_) => todo!(),
            Value::Char(_) => todo!(),
            Value::String(_) => todo!(),
            Value::Keyword(_) => todo!(),
            Value::Bytes(_) => todo!(),
            Value::Cons(_) => todo!(),
            Value::Vector(_) => todo!(),
        },
        Value::Number(nb) => Literal(nb.as_i64().unwrap() as i32),
        Value::Symbol(s) => {
            // This is a handled as a reference
            Ref(s.to_string())
        }
        _ => panic!("Loul {:?}", value),
    }
}

#[cfg(test)]
mod tests {
    use super::{parse, Expr::*, ExprResult::*, Operator::*};

    mod evaluator {

        use super::super::{parse, Expr::*, ExprResult::*, Operator::*};

        #[test]
        fn test_add() {
            let expr = BinOp {
                l: Box::new(Literal(5)),
                op: Plus,
                r: Box::new(Literal(3)),
            };
            assert_eq!(expr.eval(), Int(8));
        }

        #[test]
        fn test_sub() {
            let expr = BinOp {
                l: Box::new(Literal(5)),
                op: Minus,
                r: Box::new(Literal(7)),
            };
            assert_eq!(expr.eval(), Int(-2));
        }

        #[test]
        fn test_mal() {
            let expr = BinOp {
                l: Box::new(Literal(-9)),
                op: Multiply,
                r: Box::new(Literal(7)),
            };
            assert_eq!(expr.eval(), Int(-63));
        }

        #[test]
        fn test_div() {
            let expr = BinOp {
                l: Box::new(Literal(13)),
                op: Divide,
                r: Box::new(Literal(2)),
            };
            assert_eq!(expr.eval(), Int(6));
        }

        #[test]
        fn test_if() {
            let expr = IfExpr {
                cond: Box::new(BinOp {
                    l: Box::new(Literal(4)),
                    op: Equal,
                    r: Box::new(BinOp {
                        l: Box::new(Literal(3)),
                        op: Plus,
                        r: Box::new(Literal(1)),
                    }),
                }),
                true_branch: Box::new(Literal(5)),
                false_branch: Box::new(Literal(8)),
            };
            assert_eq!(expr.eval(), Int(5));
        }

        #[test]
        fn test_bool_literal() {
            let expr = IfExpr {
                cond: Box::new(LiteralBool(false)),
                true_branch: Box::new(Literal(5)),
                false_branch: Box::new(Literal(8)),
            };
            assert_eq!(expr.eval(), Int(8));
        }

        #[test]
        fn test_let_ref() {
            let expr = Let {
                vname: "VOTAI".to_string(),
                vval: Box::new(Literal(5)),
                code: Box::new(Ref("VOTAI".to_string())),
            };
            assert_eq!(expr.eval(), Int(5));
        }
    }

    #[test]
    fn test_parse() {
        let values =
            lexpr::from_str("(let a 12 (+ a (if true 15 18)))").unwrap();
        let expr = parse(&values);
        assert_eq!(expr.eval(), Int(27));
    }
}
