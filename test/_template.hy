load "test/helpers/test_case.hy";

# To create a new test case, simply copy this file to the correct directory and add your test functions
#
# 1. Define the name() of your test case
#
# 2. You will need to add your tests to the loadTests() function below:
#    tests = arrayAppend(tests, this.testMyNewThing);
#
# 3. Be sure to register the test class to the main test runner as follows:
#    load "test/hyde/string.hy";
#    testClass = Test;
#    runner.registerTestClass(testClass);
class Test < TestCase {
  name() {
    return "DEFINE ME!";
  }

  loadTests() {
    var tests = Array(0);

    # Register more tests here!
    # tests = arrayAppend(tests, this.testMyNewThing);

    super.loadTests(tests);
  }
}