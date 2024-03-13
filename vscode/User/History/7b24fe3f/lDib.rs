#[derive(Debug)]
pub enum Operator {
    Plus,
    Minus,
    Divide,
    Multiply,
}

#[derive(Debug)]
pub enum Expr {
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
}

pub fn eval(expr: &Expr) -> i32 {
    match expr {
        Expr::BinOp { l, op, r } => match op {
            Operator::Plus => eval(l) + eval(r),
            Operator::Minus => eval(l) - eval(r),
            Operator::Divide => eval(l) / eval(r),
            Operator::Multiply => eval(l) * eval(r),
        },
        Expr::IfExpr {
            cond,
            true_branch,
            false_branch,
        } => {
            if eval(cond) != 0 {
                eval(true_branch)
            } else {
                eval(&false_branch)
            }
        }
        Expr::Literal(x) => *x,
    }
}

#[cfg(test)]
mod tests {
    use super::{Expr::*, Operator::*, *};

    #[test]
    fn test_add() {
        let expr = BinOp {
            l: Box::new(Literal(5)),
            op: Plus,
            r: Box::new(Literal(3)),
        };
        assert_eq!(eval(&expr), 8);
    }

    #[test]
    fn test_sub() {
        let expr = BinOp {
            l: Box::new(Literal(5)),
            op: Minus,
            r: Box::new(Literal(7)),
        };
        assert_eq!(eval(&expr), -2);
    }

    #[test]
    fn test_div() {
        let expr = BinOp {
            l: Box::new(Literal(13)),
            op: Divide,
            r: Box::new(Literal(2)),
        };
        assert_eq!(eval(&expr), 6);
    }

    #[test]
    fn test_if() {
        let expr = IfExpr {
            cond: Box::new(Literal(3)),
            true_branch: Box::new(Literal(5)),
            false_branch: Box::new(Literal(8)),
        };
        assert_eq!(eval(&expr), 5);
    }
}
