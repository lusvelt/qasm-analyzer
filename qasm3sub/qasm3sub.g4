/*
This is a subset of the OpenQASM 3.0 language described here:
https://qiskit.github.io/openqasm/grammar/index.html
The following productions from the original language have not been
inserted in this version:
    * globalStatement: kernelDeclaration | calibration
    * quantumStatement: timingStatement
    * expressionTerminator: kernelCall | timingTerminator
    * kernelDeclaration
    * kernelCall
    * ** Circuit Timing ** (all productions)
    * ** Pulse Level Description ** (all productions)
    * fragment TimeUnit
    * TimingLiteral
*/

grammar qasm3sub;

/**** Parser grammar ****/

program
    : header (globalStatement | statement)*
    ;

/** Header **/
header
    : version? include*
    ;

version
    : 'OPENQASM' (Integer | RealNumber) SEMICOLON
    ;

include
    : 'include' StringLiteral SEMICOLON
    ;

/** Statements, Assignments and Return Signature **/
globalStatement
    : subroutineDefinition
    | quantumGateDefinition
	| quantumDeclarationStatement  // qubits are declared globally
    | pragma
    ;

statement
    : expressionStatement
    | assignmentStatement
    | classicalDeclarationStatement
    | branchingStatement
    | loopStatement
    | controlDirectiveStatement
    | aliasStatement
    | quantumStatement
    ;

quantumDeclarationStatement: quantumDeclaration SEMICOLON;

classicalDeclarationStatement
    : (classicalDeclaration | constantDeclaration) SEMICOLON
    ;

classicalAssignment
    : indexIdentifier assignmentOperator (expression | indexIdentifier)
    ;

assignmentStatement: (classicalAssignment | quantumMeasurementAssignment) SEMICOLON;

returnSignature
    : ARROW classicalType
    ;

/** Types and Casting **/
designator
    : LBRACKET expression RBRACKET
    ;

doubleDesignator
    : LBRACKET expression COMMA expression RBRACKET
    ;

identifierList
    : (Identifier COMMA)* Identifier
    ;

association
    : COLON Identifier
    ;

/** Quantum Types **/
quantumType
    : 'qubit'
    | 'qreg'
    ;

quantumDeclaration
    : quantumType indexIdentifierList
    ;

quantumArgument
    : quantumType designator? association
    ;

quantumArgumentList
    : (quantumArgument COMMA)* quantumArgument
    ;

/** Classical Types **/
bitType
    : 'bit'
    | 'creg'
    ;

singleDesignatorType
    : 'int'
    | 'uint'
    | 'float'
    | 'angle'
    ;

doubleDesignatorType
    : 'fixed'
    ;

noDesignatorType
    : 'bool'
    ;

classicalType
    : singleDesignatorType designator
    | doubleDesignatorType doubleDesignator
    | noDesignatorType
    | bitType designator?
    ;

constantDeclaration
    : 'const' equalsAssignmentList
    ;

// if multiple variables declared at once, either none are assigned or all are assigned prevents
// ambiguity w/ qubit arguments in subroutine calls
singleDesignatorDeclaration
    : singleDesignatorType designator (identifierList | equalsAssignmentList)
    ;

doubleDesignatorDeclaration
    : doubleDesignatorType doubleDesignator (identifierList | equalsAssignmentList)
    ;

noDesignatorDeclaration
    : noDesignatorType (identifierList | equalsAssignmentList)
    ;

bitDeclaration
    : bitType (indexIdentifierList | indexEqualsAssignmentList)
    ;

classicalDeclaration
    : singleDesignatorDeclaration
    | doubleDesignatorDeclaration
    | noDesignatorDeclaration
    | bitDeclaration
    ;
/*
classicalTypeList
    : (classicalType COMMA)* classicalType
    ;
*/
classicalArgument
    : classicalType association
    ;

classicalArgumentList
    : (classicalArgument COMMA)* classicalArgument
    ;

/** Aliasing **/
aliasStatement
    : 'let' Identifier EQUALS indexIdentifier SEMICOLON
    ;

/** Register Concatenation and Slicing **/
indexIdentifier
    : Identifier rangeDefinition
    | Identifier (LBRACKET expressionList RBRACKET)?
    | indexIdentifier '||' indexIdentifier
    ;

indexIdentifierList
    : (indexIdentifier COMMA)* indexIdentifier
    ;

indexEqualsAssignmentList
    : (indexIdentifier equalsExpression COMMA)* indexIdentifier equalsExpression
    ;

rangeDefinition
    : LBRACKET expression? COLON expression? (COLON expression)? RBRACKET
    ;

/*** Gates and Built-in Quantum Instructions ***/
quantumGateDefinition
    : 'gate' quantumGateSignature quantumBlock
    ;

quantumGateSignature
    : (Identifier | 'CX' | 'U') (LPAREN identifierList? RPAREN)? identifierList
    ;

quantumBlock
    : LBRACE (quantumStatement | quantumLoop)* RBRACE
    ;

// loops containing only quantum statements allowed in gates
quantumLoop
    : loopSignature quantumLoopBlock
    ;

quantumLoopBlock
    : quantumStatement
    | LBRACE quantumStatement* RBRACE
    ;

quantumStatement
    : quantumInstruction SEMICOLON
    ;

quantumInstruction
    : quantumGateCall
    | quantumPhase
    | quantumMeasurement
    | quantumBarrier
    ;

quantumPhase
    : 'gphase' LPAREN Identifier RPAREN
    ;

quantumMeasurement
    : 'measure' indexIdentifierList
    ;

quantumMeasurementAssignment
    : quantumMeasurement (ARROW indexIdentifierList)?
    | indexIdentifierList EQUALS quantumMeasurement
    ;

quantumBarrier
    : 'barrier' indexIdentifierList
    ;

quantumGateModifier
    : ('inv' | 'pow' LPAREN expression RPAREN | 'ctrl') '@'
    ;

quantumGateCall
    : quantumGateName (LPAREN expressionList? RPAREN)? indexIdentifierList
    ;

quantumGateName
    : 'CX'
    | 'U'
    | 'reset'
    | Identifier
    | quantumGateModifier quantumGateName
    ;

/*** Classical Instructions ***/
unaryOperator
    : '~' | '!'
    ;

relationalOperator
    : '>'
    | '<'
    | '>='
    | '<='
    | '=='
    | '!='
    ;

logicalOperator
    : '&&'
    | '||'
    ;

expressionStatement
    : expression SEMICOLON
    ;

expression
    // include terminator/unary as base cases to simplify parsing
    : expressionTerminator
    | unaryExpression
    // expression hierarchy
    | xOrExpression
    | expression '|' xOrExpression
    ;

/**  Expression hierarchy for non-terminators. Adapted from ANTLR4 C
  *  grammar: https://github.com/antlr/grammars-v4/blob/master/c/C.g4
  * Order (first to last evaluation):
    Terminator (including Parens),
    Unary Op,
    Multiplicative
    Additive
    Bit Shift
    Bit And
    Exlusive Or (xOr)
    Bit Or
**/
xOrExpression
    : bitAndExpression
    | xOrExpression '^' bitAndExpression
    ;

bitAndExpression
    : bitShiftExpression
    | bitAndExpression '&' bitShiftExpression
    ;

bitShiftExpression
    : additiveExpression
    | bitShiftExpression ('<<' | '>>') additiveExpression
    ;

additiveExpression
    : multiplicativeExpression
    | additiveExpression (PLUS | MINUS) multiplicativeExpression
    ;

multiplicativeExpression
    // base case either terminator or unary
    : expressionTerminator
    | unaryExpression
    | multiplicativeExpression (MUL | DIV | MOD) (expressionTerminator | unaryExpression)
    ;

unaryExpression
    : unaryOperator expressionTerminator
    ;

expressionTerminator
    : Constant
    | Integer
    | RealNumber
    | Identifier
    | StringLiteral
    | builtInCall
    | subroutineCall
    | MINUS expressionTerminator
    | LPAREN expression RPAREN
    | expressionTerminator LBRACKET expression RBRACKET
    | expressionTerminator incrementor
    ;
/** End expression hierarchy ***/

incrementor
    : '++'
    | '--'
    ;

builtInCall
    : (builtInMath | castOperator) LPAREN expressionList RPAREN
    ;

builtInMath
    : 'sin' | 'cos' | 'tan' | 'exp' | 'ln' | 'sqrt' | 'rotl' | 'rotr' | 'popcount' | 'lengthof'
    ;

castOperator
    : classicalType
    ;

expressionList
    : (expression COMMA)* expression
    ;

/** Boolean expression hierarchy **/
booleanExpression
    : membershipTest
    | comparisonExpression
    | booleanExpression logicalOperator comparisonExpression
    ;

comparisonExpression
    : expression  // if (expression)
    | expression relationalOperator expression
    ;
/** End boolean expression hierarchy **/

equalsExpression
    : EQUALS expression
    ;

assignmentOperator
    : EQUALS
    | '+=' | '-=' | '*=' | '/=' | '&=' | '|=' | '~=' | '^=' | '<<=' | '>>='
    ;

equalsAssignmentList
    : (Identifier equalsExpression COMMA)* Identifier equalsExpression
    ;

membershipTest
    : Identifier 'in' setDeclaration
    ;

setDeclaration
    : LBRACE expressionList RBRACE
    | rangeDefinition
    | Identifier
    ;

programBlock
    : statement
    | LBRACE statement* RBRACE
    ;

branchingStatement
    : 'if' LPAREN booleanExpression RPAREN programBlock ('else' programBlock)?
    ;

loopSignature
    : ('#invariant' COLON booleanExpression)? 'for' membershipTest
    | ('#invariant' COLON booleanExpression)? 'while' LPAREN booleanExpression RPAREN
    ;

loopStatement: loopSignature programBlock;

controlDirectiveStatement
    : controlDirective SEMICOLON
    ;

controlDirective
    : 'break'
    | 'continue'
    | 'end'
    ;

/*** Subroutines ***/
subroutineDefinition
    : ('#qubits' expression)? 'def' Identifier (LPAREN classicalArgumentList? RPAREN)? quantumArgumentList?
    returnSignature? subroutineBlock
    ;

returnStatement: 'return' statement;

subroutineBlock
    : LBRACE statement* returnStatement? RBRACE
    ;

// if have subroutine w/ out args, is ambiguous; may get matched as identifier
subroutineCall
    : Identifier (LPAREN expressionList? RPAREN)? indexIdentifierList
    ;

/** Directives **/
pragma
    : '#pragma' LBRACE statement* RBRACE // match any valid openqasm statements
    ;

/***** Lexer grammar ****/

LBRACKET: '[';
RBRACKET: ']';

LBRACE: '{';
RBRACE: '}';

LPAREN: '(';
RPAREN: ')';

COLON: ':';
SEMICOLON: ';';

DOT: '.';
COMMA: ',';

EQUALS: '=';
ARROW: '->';

PLUS: '+';
MINUS: '-';
MUL: '*';
DIV: '/';
MOD: '%';


Constant: ('pi' | 'π' | 'tau' | '𝜏' | 'euler' | 'ℇ');

Whitespace: [ \t]+ -> skip;
Newline: [\r\n]+ -> skip;

fragment Digit: [0-9];
Integer: Digit+;

fragment ValidUnicode: [\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}]; // valid unicode chars
fragment Letter: [A-Za-z];
fragment FirstIdCharacter: '_' | '$' | ValidUnicode | Letter;
fragment GeneralIdCharacter: FirstIdCharacter | Integer;

Identifier: FirstIdCharacter GeneralIdCharacter*;

fragment SciNotation: [eE];
fragment PlusMinus: PLUS | MINUS;
fragment Float: Digit+ DOT Digit*;
RealNumber: Float (SciNotation PlusMinus? Integer)?;

StringLiteral
    : '"' ~["\r\t\n]+? '"'
    | '\'' ~['\r\t\n]+? '\''
    ;

LineComment: '//' ~[\r\n]* -> skip;
BlockComment: '/*' .*? '*/' -> skip;
