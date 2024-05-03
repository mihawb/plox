# plox
My implementation of the interpreter (and hopefully the compiler too, later on) for Lox language created by Robert Nystrom for his book [Crafting Interpreters](https://craftinginterpreters.com/).  

## Implementations 
On branch `jlox-carbon-copy` I directly copied the original interpreter written in Java. Only minimal changes were applied, leaving it in OOP style.  
  
On `main` branch resides a proper pythonic port of the interpreter, with the following changes:
* lexer accepting multiline comments 
* the Visitor Pattern removed since Python doesn't need to *mimic* functional programming style - it has strong support for FP paradigm
* structural pattern matching in place of VP
* better metaprogramming macros for AST generation
* more changes under way, as it's still work in progress

I also plan to port the compiler from C to Rust, given this project doesn't bore me to death midway through as they all usually do, unfortunately.