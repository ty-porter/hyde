load "test/helpers/test_case.hy";

class Test < TestCase {
  name() {
    return "Number";
  }

  testLiteral() {
    var literal = 1;

    return super.assertEquals(literal, 1);
  }

  testAdditionOperand() {
    var num1 = 1;
    var num2 = 2;

    return super.assertEquals(num1 + num2, 3);
  }

  testSubtractionOperand() {
    var num1 = 2;
    var num2 = 1;

    return super.assertEquals(num1 - num2, 1);
  }

  testMultiplicationOperand() {
    var num1 = 4;
    var num2 = 3;

    return super.assertEquals(num1 * num2, 12);
  }

  testDivisionOperand() {
    var num1 = 15;
    var num2 = 5;

    return super.assertEquals(num1 / num2, 3);
  }

  loadTests() {
    var tests = Array(0);

    tests = arrayAppend(tests, this.testLiteral);
    tests = arrayAppend(tests, this.testAdditionOperand);
    tests = arrayAppend(tests, this.testSubtractionOperand);
    tests = arrayAppend(tests, this.testMultiplicationOperand);
    tests = arrayAppend(tests, this.testDivisionOperand);

    super.loadTests(tests);
  }
}