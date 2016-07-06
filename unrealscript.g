start: program;

program: classdecl (declaration)* (replicationblock)? body;

classdecl: CLASS identifier (EXTENDS type)? (classparams)* SEMICOLON;

classparams: constclassparams |
             within  |
             dependson|
             config |
             hidecategories |
             showcategories
             ;

config: CONFIG (LBRACK packageidentifier RBRACK)?;

hidecategories: HIDECATEGORIES LBRACK identifierlist RBRACK;

showcategories: SHOWCATEGORIES LBRACK identifierlist RBRACK;

dependson: DEPENDSON LBRACK packageidentifier RBRACK;

within: WITHIN packageidentifier;

constclassparams: ABSTRACT | NATIVE | NATIVEREPLICATION | SAFEREPLACE |
                  PEROBJECTCONFIG | TRANSIENT | NOEXPORT | EXPORTSTRUCTS |
                  GUID LBRACK intval COMMA intval COMMA intval COMMA intval RBRACK |
                  COLLAPSECATEGORIES | DONTCOLLAPSECATEGORIES | PLACEABLE |
                  NOTPLACEABLE | EDITINLINENEW | NOTEDITINLINENEW
                  ;

packageidentifier: ( identifier DOT )? identifier;

identifier: IDENTIFIER;

identifierlist: identifier
              | identifier COMMA identifierlist
              ;

type: identifier;

IDENTIFIER: '[a-zA-Z_][a-zA-Z_0-9]*'
            (%unless
                CLASS: 'class';
                EXTENDS: 'extends';

                VAR: 'var';
                ENUM: 'enum';
                STRUCT: 'struct';

                TRUE: 'true';
                FALSE: 'false';

                BYTE: 'byte';
                INT: 'int';
                FLOAT: 'float';
                STRING: 'string';
                BOOL: 'bool';
                NAME: 'name';

                CONFIG: 'config';
                CONST: 'const';
                EDITCONST: 'editconst';
                EXPORT: 'export';
                GLOBALCONFIG: 'globalconfig';
                INPUT: 'input';
                LOCALIZED: 'localized';
                NATIVE: 'native';
                PRIVATE: 'private';
                PROTECTED: 'protected';
                TRANSIENT: 'transient';
                TRAVEL: 'travel';
                EDITINLINE: 'editinline';
                DEPRECATED: 'deprecated';
                EDFINDABLE: 'edfindable';
                EDITINLINEUSE: 'editinlineuse';

                ARRAY: 'array';

                WITHIN: 'within';
                DEPENDSON: 'dependson';
                HIDECATEGORIES: 'hidecategories';
                SHOWCATEGORIES: 'showcategories';

                ABSTRACT: 'abstract';
                NATIVEREPLICATION: 'nativereplication';
                SAFEREPLACE: 'safereplace';
                PEROBJECTCONFIG: 'perobjectconfig';
                NOEXPORT: 'noexport';
                EXPORTSTRUCTS: 'exportstructs';
                COLLAPSECATEGORIES: 'collapsecategories';
                DONTCOLLAPSECATEGORIES: 'dontcollapsecategories';
                PLACEABLE: 'placeable';
                NOTPLACEABLE: 'notplaceable';
                EDITINLINENEW: 'editinlinenew';
                NOTEDITINLINENEW: 'noteditinlinenew';

                REPLICATION: 'replication';
                RELIABLE: 'reliable';
                UNRELIABLE: 'unreliable';
                DEFAULT: 'default';
                STATIC: 'static';

                IGNORES: 'ignores';
                STATE: 'state';

                GUID: 'guid';

                IF: 'if';
                DO: 'do';
                UNTIL: 'until';
                FOREACH: 'foreach';
                RETURN: 'return';
                SWITCH: 'switch';
                CASE: 'case';
                WHILE: 'while';

                FOR: 'for';

                AUTO: 'auto';
                SIMULATED: 'simulated';

                FINAL: 'final';
                EVENT: 'event';
                DELEGATE: 'delegate';
                EXEC: 'exec';
                SINGULAR: 'singular';
                ITERATOR: 'iterator';
                LATENT: 'latent';
                FUNCTION: 'function';
                LOCAL: 'local';

                COERCE: 'coerce';
                OPTIONAL: 'optional';
                OUT: 'out';

                OPERATOR: 'operator';
                PREOPERATOR: 'preoperator';
                POSTOPERATOR: 'postoperator';
            )
            ;

declaration: ( constdecl | vardecl | enumdecl | structdecl) SEMICOLON;

constdecl: CONST identifier ASSIGN constvalue;

constvalue: (stringval | intval | floatval | boolval);

configgroup: LBRACK (identifier)? RBRACK;

vardecl: VAR (configgroup)? (varparams)* vartype varidentifier (COMMA varidentifier)*;

vartype: packageidentifier |
         enumdecl |
         structdecl |
         classtype |
         arraytype |
         basictype
         ;

varparams: CONFIG |
           CONST |
           EDITCONST |
           EXPORT |
           GLOBALCONFIG |
           INPUT |
           LOCALIZED |
           NATIVE |
           PRIVATE |
           PROTECTED |
           TRANSIENT |
           TRAVEL |
           EDITINLINE |
           DEPRECATED |
           EDFINDABLE |
           EDITINLINEUSE
           ;

arraytype: ARRAY LABRACK (packageidentifier | classtype | basictype) RABRACK;

varidentifier: identifier (LSBRACK (intval | identifier) RSBRACK)?;

basictype: BYTE |
           INT |
           FLOAT |
           STRING |
           BOOL |
           NAME |
           CLASS
           ;

classtype: CLASS LABRACK packageidentifier RABRACK;

enumdecl: ENUM identifier LCBRACK enumoptions RCBRACK;

enumoptions: identifier (COMMA identifier)*;

structdecl: STRUCT (structparams)* identifier (EXTENDS packageidentifier)? LCBRACK structbody RCBRACK;

structparams: NATIVE | EXPORT;

structbody: (vardecl SEMICOLON)+;

stringval: '"((\\{2})*|(.*?[^\\](\\{2})*))"';
intval: '[-+]?\d+';
floatval: '[-+]?\d*?[.]\d+';
boolval: TRUE | FALSE;

replicationblock: REPLICATION LCBRACK (replicationbody)* RCBRACK;

replicationbody: (RELIABLE | UNRELIABLE) IF LBRACK expr RBRACK identifier (COMMA identifier)* SEMICOLON;

expr: operand (opidentifier operand)*;

operand: (constvalue | qualifiedidentifier | funccall | subscription);

subscription: operand LSBRACK expr RSBRACK;

funccall: ((CLASS SQUOTE packageidentifier SQUOTE DOT STATIC DOT) | ( ( identifier DOT )+))? identifier LBRACK (expr (COMMA expr)*)? RBRACK;

qualifiedidentifier: ((CLASS SQUOTE packageidentifier SQUOTE DOT DEFAULT DOT identifier) | ((identifier DOT)* identifier));

opidentifier: identifier | operatornames;

operatornames: BITWISE_NOT | NOT | CONCATENATE_SPACE | CONCATENATE | MODULO |
               BITWISE_XOR | BITWISE_AND | MULTIPLY | MINUS | ASSIGN | PLUS |
               BITWISE_OR | COLON | LABRACK | RABRACK | FSLASH | GRAVE |
               LSHIFT | RSHIFT | NEQUAL | LTEQUAL | GTEQUAL | INCREMENT |
               DECREMENT | ADDASSIGN | SUBASSIGN | MULASSIGN | DIVASSIGN |
               LOGICAL_AND | LOGICAL_OR | LOGICAL_XOR | EQUAL | EXPONENT |
               ALMOSTEQUAL | CONCATENATE_ASSIGN | RSHIFT2;

body: (statedecl | functiondecl)*;

statedecl: (stateparams)* STATE identifier (configgroup)? (EXTENDS identifier)? statebody;
statebody: LCBRACK (stateignore)? (functiondecl)* statelabels RCBRACK;
stateignore: IGNORES identifier (COMMA identifier)* SEMICOLON;
statelabels: (identifier COLON (codeline)*)*;
stateparams: AUTO | SIMULATED;

codeline: (statement | assignment | ifthenelse | whileloop | doloop |
           switchcase | returnfunc | foreachloop | forloop);

codeblock: (codeline | (LCBRACK (codeline)* RCBRACK));

statement: funccall SEMICOLON;
assignment: expr ASSIGN expr SEMICOLON;
ifthenelse: IF LBRACK expr RBRACK codeblock;
whileloop: WHILE LBRACK expr RBRACK codeblock;
doloop: DO codeblock UNTIL LBRACK expr RBRACK;
switchcase: SWITCH LBRACK expr RBRACK LCBRACK (caserule)+ (defaultrule)? RCBRACK;
caserule: CASE intval COLON codeblock;
defaultrule: DEFAULT codeblock;
returnfunc: RETURN (expr)? SEMICOLON;
foreachloop: FOREACH funccall codeblock;
forloop: FOR LBRACK assignment SEMICOLON expr SEMICOLON expr RBRACK codeblock;

functiondecl: (normalfunc | operatorfunc);

normalfunc: (functionparams)* functiontype (localtype)? identifier LBRACK (functionargs (COMMA functionargs)*)? RBRACK functionbody;
functionparams: constfuncparams | NATIVE (LBRACK intval RBRACK)?;
constfuncparams: FINAL | ITERATOR | LATENT | SIMULATED | SINGULAR | STATIC | EXEC | PROTECTED | PRIVATE;
functiontype: FUNCTION | EVENT | DELEGATE;
functionbody: SEMICOLON | LCBRACK ((localdecl)* (codeline)*) RCBRACK;
localtype: packageidentifier | arraytype | classtype | basictype;
localdecl: LOCAL localtype varidentifier ( COMMA varidentifier )* SEMICOLON;
functionargs: (functionargparams)? functionargtype identifier;
functionargtype: packageidentifier | arraytype | classtype | basictype;
functionargparams: OPTIONAL | OUT | COERCE;

operatorfunc: (functionparams)* operatortype functionbody;
operatortype: (binaryoperator | unaryoperator);
binaryoperator: OPERATOR LBRACK intval RBRACK packageidentifier opidentifier LBRACK functionargs COMMA functionargs RBRACK;
unaryoperator: (PREOPERATOR | POSTOPERATOR) packageidentifier opidentifier LBRACK functionargs RBRACK;

WS: '[\s]+' (%ignore);
COMMENT: '(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)' (%ignore);

ALPHA: '[a-z]';
DIGIT: '[0-9]';
SEMICOLON: '\;';
COLON: ':';
UNDERSCORE: '_';
LBRACK: '\(';
RBRACK: '\)';
LABRACK: '<';
RABRACK: '>';
LCBRACK: '{';
RCBRACK: '}';
LSBRACK: '\[';
RSBRACK: ']';
DOT: '.';
COMMA: ',';
SQUOTE: ''';
DQUOTE: '"';
ASSIGN: '=';
FSLASH: '/';
GRAVE: '`';
LSHIFT: '<<';
RSHIFT: '>>';
NEQUAL: '!=';
LTEQUAL: '<=';
GTEQUAL: '>=';
INCREMENT: '\+\+';
DECREMENT: '--';
MINUS: '-';
PLUS: '\+';
LOGICAL_AND: '&&';
LOGICAL_OR: '\|\|';
ADDASSIGN: '\+=';
SUBASSIGN: '-=';
MULASSIGN: '\*=';
DIVASSIGN: '/=';
CONCATENATE: '\$';
CONCATENATE_ASSIGN: '$=';
CONCATENATE_SPACE: '@';
CONCATENATE_SPACE_ASSIGN: '@=';
EQUAL: '==';
ALMOSTEQUAL: '~=';
RSHIFT2: '>>>';
NOT: '!';
BITWISE_NOT: '~';
MODULO: '%';
BITWISE_AND: '&';
BITWISE_OR: '\|';
MULTIPLY: '\*';
EXPONENT: '\*\*';
LOGICAL_XOR: '\^\^';
BITWISE_XOR: '\^';
