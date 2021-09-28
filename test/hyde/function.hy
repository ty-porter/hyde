load "test/helpers/test_case.hy";

class Test < TestCase {
  name() {
    return "Function";
  }

  testFunctionDeclaration() {
    fun testFunction() {}

    return super.assert(True);
  }

  testFunctionCall() {
    fun testFunction() {
      return True;
    }

    return super.assert(testFunction());
  }
  
  testFunctionCallWithArgs() {
    fun testFunction(arg1, arg2) {
      return arg1;
    }

    return super.assert(testFunction(True, True));
  }

  testEarlyReturn() {
    return super.assert(True);
    return super.assert(False);
  }

  testRecursion() {
    # sums all numbers between start and stop, adds to counter
    fun sumBetween(start, stop, counter) {
      if (stop < start) {
        return counter;
      }

      return sumBetween(start, stop - 1, counter + stop);
    }

    var value = sumBetween(1, 10, 0);

    return super.assertEquals(value, 55);
  }

  testClosures() {
    fun makeCounter() {
      var i = 0;

      fun count() {
        i = i + 1;
        return i;
      }

      return count;
    }

    var counter = makeCounter();

    var num1 = counter();
    var num2 = counter();

    if (num1 == 1 and num2 == 2) {
      return super.assert(True);
    } else {
      return super.assert(False);
    }
  }

  loadTests() {
    var tests = Array(0);

    tests = arrayAppend(tests, this.testFunctionDeclaration);
    tests = arrayAppend(tests, this.testFunctionCall);
    tests = arrayAppend(tests, this.testFunctionCallWithArgs);
    tests = arrayAppend(tests, this.testEarlyReturn);
    tests = arrayAppend(tests, this.testRecursion);
    tests = arrayAppend(tests, this.testClosures);

    super.loadTests(tests);
  }
}