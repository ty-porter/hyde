load "test/test_runner.hy";

var runner = TestRunner();
var testClass;

load "test/hyde/string.hy";
testClass = Test;
runner.registerTestClass(testClass);

load "test/hyde/number.hy";
testClass = Test;
runner.registerTestClass(testClass);

load "test/hyde/scope.hy";
testClass = Test;
runner.registerTestClass(testClass);

load "test/hyde/control_flow.hy";
testClass = Test;
runner.registerTestClass(testClass);

load "test/hyde/globals.hy";
testClass = Test;
runner.registerTestClass(testClass);

load "test/hyde/array.hy";
testClass = Test;
runner.registerTestClass(testClass);

load "test/hyde/map.hy";
testClass = Test;
runner.registerTestClass(testClass);

load "test/hyde/function.hy";
testClass = Test;
runner.registerTestClass(testClass);

load "test/hyde/class.hy";
testClass = Test;
runner.registerTestClass(testClass);

runner.run();