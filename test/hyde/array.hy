load "test/helpers/test_case.hy";

class Test < TestCase {
  name() {
    return "Array";
  }
  
  testArraySetAndGet() {
    var array = Array(1);
    array.set(0, True);

    return super.assert(array.get(0));
  }

  testArrayConcat() {
    var array1 = Array(1);
    var array2 = Array(1);

    array1.set(0, True);
    array2.set(0, True);

    var expectedSize = array1.length() + array2.length();

    var array3 = arrayConcat(array1, array2);

    if (array3.length() != expectedSize) {
      return super.assert(False);
    }

    for (var i = 0; i < expectedSize; i = i + 1) {
      if (array3.get(i) != True) {
        return super.assert(False);
      }
    }

    return super.assert(True);
  }

  testArrayAppend() {
    var array1 = Array(1);

    array1.set(0, True);

    var expectedSize = array1.length() + 1;

    var array2 = arrayAppend(array1, True);

    if (array2.length() != expectedSize) {
      return super.assert(False);
    }

    for (var i = 0; i < expectedSize; i = i + 1) {
      if (array2.get(i) != True) {
        return super.assert(False);
      }
    }

    return super.assert(True);
  }

  loadTests() {
    var tests = Array(0);

    tests = arrayAppend(tests, this.testArraySetAndGet);
    tests = arrayAppend(tests, this.testArrayConcat);
    tests = arrayAppend(tests, this.testArrayAppend);

    super.loadTests(tests);
  }
}