load "test/helpers/test_case.hy";

class Test < TestCase {
  name() {
    return "Control Flow";
  }

  testTrueIfCondition() {
    if (True) {
      return super.assert(True);
    }

    return super.assert(False);
  }

  testFalseIfCondition() {
    if (False) {
      return super.assert(False);
    }

    return super.assert(True);
  }

  testElseCondition() {
    if (False) {
      return super.assert(False);
    } else {
      return super.assert(True);
    }
  }

  testForLoop() {
    var sum = 0;

    for (var i = 0; i < 10; i = i + 1) {
      sum = sum + 1;
    }

    return super.assertEquals(sum, 10);
  }

  testWhileLoop() {
    var n = 0;

    while (n < 10) {
      n = n + 1;
    }

    return super.assertEquals(n, 10);
  }

  testFibonacci() {
    var a = 0;
    var temp;

    for (var b = 1; a < 10000; b = temp + b) {
      temp = a;
      a = b;
    }

    return super.assertEquals(a, 10946);
  }

  loadTests() {
    var tests = Array(0);

    tests = arrayAppend(tests, this.testTrueIfCondition);
    tests = arrayAppend(tests, this.testFalseIfCondition);
    tests = arrayAppend(tests, this.testElseCondition);
    tests = arrayAppend(tests, this.testForLoop);
    tests = arrayAppend(tests, this.testWhileLoop);
    tests = arrayAppend(tests, this.testFibonacci);

    super.loadTests(tests);
  }
}