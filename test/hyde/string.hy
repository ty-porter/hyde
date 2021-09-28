load "test/helpers/test_case.hy";

class Test < TestCase {
  name() {
    return "String";
  }

  testLiteral() {
    var literal = "Literal";

    return super.assertEquals(literal, "Literal");
  }

  testConcatOperand() {
    var string1 = "test";
    var string2 = "test";

    return super.assertEquals(string1 + string2, "testtest");
  }

  loadTests() {
    var tests = Array(0);

    tests = arrayAppend(tests, this.testLiteral);
    tests = arrayAppend(tests, this.testConcatOperand);

    super.loadTests(tests);
  }
}