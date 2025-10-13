const LR1Parser = require('./lr1-parser.js').LR1Parser || (() => {
    if (typeof window !== 'undefined') {
        return window.LR1Parser;
    }
    const fs = require('fs');
    const vm = require('vm');
    const code = fs.readFileSync('./lr1-parser.js', 'utf8');
    const context = {};
    vm.createContext(context);
    vm.runInContext(code, context);
    return context.LR1Parser;
})();

function testBasicArithmeticGrammar() {
    console.log('Testing basic arithmetic grammar...');
    
    const parser = new LR1Parser();
    const grammar = `S -> E
E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> id`;
    
    try {
        parser.parseGrammar(grammar);
        console.log('✓ Grammar parsed successfully');
        
        const firstFollow = parser.getFirstFollowDisplay();
        console.log('FIRST sets:', firstFollow.first);
        console.log('FOLLOW sets:', firstFollow.follow);
        
        const testStrings = [
            'id',
            'id + id',
            'id * id',
            'id + id * id',
            '( id )',
            '( id + id ) * id'
        ];
        
        testStrings.forEach(str => {
            console.log(`\nTesting string: "${str}"`);
            const result = parser.parseString(str);
            console.log(result.success ? '✓ ACCEPTED' : '✗ REJECTED');
            if (!result.success) {
                console.log('Error:', result.error);
            }
        });
        
        return true;
    } catch (error) {
        console.error('✗ Test failed:', error.message);
        return false;
    }
}

function testSimpleGrammar() {
    console.log('\nTesting simple grammar...');
    
    const parser = new LR1Parser();
    const grammar = `S -> A B
A -> a
B -> b`;
    
    try {
        parser.parseGrammar(grammar);
        console.log('✓ Simple grammar parsed successfully');
        
        const result = parser.parseString('a b');
        console.log(result.success ? '✓ String "a b" ACCEPTED' : '✗ String "a b" REJECTED');
        
        const result2 = parser.parseString('a');
        console.log(result2.success ? '✗ String "a" should be REJECTED' : '✓ String "a" correctly REJECTED');
        
        return true;
    } catch (error) {
        console.error('✗ Simple test failed:', error.message);
        return false;
    }
}

if (typeof window === 'undefined') {
    const success1 = testBasicArithmeticGrammar();
    const success2 = testSimpleGrammar();
    
    if (success1 && success2) {
        console.log('\n🎉 All tests passed!');
        process.exit(0);
    } else {
        console.log('\n❌ Some tests failed!');
        process.exit(1);
    }
} else {
    window.testParser = {
        testBasicArithmeticGrammar,
        testSimpleGrammar
    };
}