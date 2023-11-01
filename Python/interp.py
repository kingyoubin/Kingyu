from typing import Any, Dict
from dataclasses import dataclass
from enum import Enum

# Constants
@dataclass
class Const:
    pass

@dataclass
class CInt(Const):
    value: int

@dataclass
class CBool(Const):
    value: bool

# Types
class Type:
    pass

class TyInt(Type):
    pass

class TyBool(Type):
    pass

# Operators
class Op(Enum):
    Add = '+'
    Sub = '-'
    Mul = '*'
    Div = '/'
    Mod = '%'
    LessThan = '<'
    Equal = '=='
    And = '&&'
    Or = '||'
    Not = 'not'

# Expressions
@dataclass
class Expr:
    pass

@dataclass
class ECst(Expr):
    value: Const

@dataclass
class EVar(Expr):
    var_name: str

@dataclass
class EBinOp(Expr):
    op: Op
    left: Expr
    right: Expr

@dataclass
class EUnaryOp(Expr):
    op: Op
    expr: Expr

# Commands
@dataclass
class Comm:
    pass

@dataclass
class CSkip(Comm):
    pass

@dataclass
class CSeq(Comm):
    comm1: Comm
    comm2: Comm

@dataclass
class CAssign(Comm):
    var_name: str
    expr: Expr

@dataclass
class CRead(Comm):
    var_name: str

@dataclass
class CWrite(Comm):
    expr: Expr

@dataclass
class CIf(Comm):
    expr: Expr
    comm1: Comm
    comm2: Comm

@dataclass
class CWhile(Comm):
    expr: Expr
    comm: Comm

@dataclass
class CAssert(Comm):
    expr: Expr

# Environment
Env = Dict[str, Any]

# Interpreter
def interp_const(const: Const) -> Any:
    if isinstance(const, CInt):
        return const.value
    if isinstance(const, CBool):
        return const.value

def interp_expr(env: Env, expr: Expr) -> Any:
    if isinstance(expr, ECst):
        return interp_const(expr.value)
    if isinstance(expr, EVar):
        var_name = expr.var_name
        if var_name in env:
            return env[var_name]
        else:
            raise ValueError(f"Variable not found: {var_name}")
    if isinstance(expr, EBinOp):
        left_val = interp_expr(env, expr.left)
        right_val = interp_expr(env, expr.right)
        op = expr.op
        if op == Op.Add:
            return left_val + right_val
        elif op == Op.Sub:
            return left_val - right_val
        elif op == Op.Mul:
            return left_val * right_val
        # Add other binary operations here...
    if isinstance(expr, EUnaryOp):
        sub_expr_val = interp_expr(env, expr.expr)
        op = expr.op
        if op == Op.Not:
            return not sub_expr_val
        # Add other unary operations here...

def interp_comm(env: Env, comm: Comm) -> Env:
    if isinstance(comm, CSkip):
        return env
    if isinstance(comm, CSeq):
        env = interp_comm(env, comm.comm1)
        env = interp_comm(env, comm.comm2)
        return env
    if isinstance(comm, CAssign):
        var_name = comm.var_name
        expr_val = interp_expr(env, comm.expr)
        env[var_name] = expr_val
        return env
    if isinstance(comm, CRead):
        var_name = comm.var_name
        try:
            value = int(input(f"Enter a value for {var_name}: "))
            env[var_name] = value
        except ValueError:
            print(f"Invalid input for {var_name}. Please enter an integer.")
        return env
    if isinstance(comm, CWrite):
        expr_val = interp_expr(env, comm.expr)
        print(expr_val)
        return env
    if isinstance(comm, CIf):
        condition = interp_expr(env, comm.expr)
        if isinstance(condition, bool):
            if condition:
                return interp_comm(env, comm.comm1)
            else:
                return interp_comm(env, comm.comm2)
        else:
            print("Error: Condition in CIf must be a boolean expression.")
            return env
    if isinstance(comm, CWhile):
        condition = interp_expr(env, comm.expr)
        if isinstance(condition, bool):
            while condition:
                env = interp_comm(env, comm.comm)
                condition = interp_expr(env, comm.expr)
            return env
        else:
            print("Error: Condition in CWhile must be a boolean expression.")
            return env
    if isinstance(comm, CAssert):
        condition = interp_expr(env, comm.expr)
        if isinstance(condition, bool):
            if not condition:
                print(f"Assertion failed: {comm.expr}")
            return env
        else:
            print("Error: Condition in CAssert must be a boolean expression.")
            return env

# Example While program
progDecls = []
progComms = [
    CAssign("x", ECst(CInt(5))),
    CAssign("y", ECst(CInt(7))),
    CAssign("z", EBinOp(Op.Add, EVar("x"), EVar("y"))),
    CWrite(EVar("z")),
    CIf(EVar("z"), CWrite(ECst(CBool(True))), CWrite(ECst(CBool(False)))
)]

env = {}
for comm in progComms:
    env = interp_comm(env, comm)