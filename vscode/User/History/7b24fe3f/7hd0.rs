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
        Expr::BinOp { l, op, r } => {
            match op {
                Operator::Plus => eval(l) + eval(r),
                Operator::Minus => eval(l) - eval(r),
                Operator::Divide => eval(l) / eval(r),
                Operator::Multiply => eval(l) * eval(r),
            }
        }
        Expr::IfExpr { cond, true_branch, false_branch } => {
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
    use super::{*, Expr::*, Operator::*};

    #[test]
    fn test_add() {
        let expr = BinOp { l: Literal(5), op: (), r: () }
    }
}
