1. Taint analysis to remove statement unrelated to output.

1. Remove useless move: for `a -> b; b -> c; c -> a`, remove `c -> a`

1. Remove `a = f(b)` if `a` is never used again or reassigned before usage.