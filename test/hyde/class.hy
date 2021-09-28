load "test/helpers/test_case.hy";

class Parent {
  inheritedMethod() {
    return "inheritedMethod";
  }

  overriddenMethod() {
    return "original";
  }

  superMethod() {
    return "superMethod";
  }
}

class Child < Parent {
  init() {
    this.existingProperty = True;
  }

  thisMethod() {
    return "thisMethod";
  }

  overriddenMethod() {
    return "overridden";
  }

  callSuperMethod() {
    return super.superMethod();
  }
}

class Test < TestCase {
  name() {
    return "Class";
  }

  testInheritance() {
    var child = Child();
    var parent = Parent();

    return super.assert(True);
  }

  testInheritedMethod() {
    var child = Child();

    return super.assertEquals(child.inheritedMethod(), "inheritedMethod");
  }

  testThisMethod() {
    var child = Child();

    return super.assertEquals(child.thisMethod(), "thisMethod");
  }

  testSuperMethod() {
    var child = Child();

    return super.assertEquals(child.callSuperMethod(), "superMethod");
  }

  testOverriddenMethodInChild() {
    var child = Child();

    return super.assertEquals(child.overriddenMethod(), "overridden");
  }

  testOverriddenMethodInParent() {
    var parent = Parent();

    return super.assertEquals(parent.overriddenMethod(), "original");
  }

  testProperties() {
    var child = Child();

    return super.assert(child.existingProperty);
  }

  testSetProperties() {
    var child = Child();
    child.newProperty = True;

    return super.assert(child.newProperty);
  }

  loadTests() {
    var tests = Array(0);

    tests = arrayAppend(tests, this.testInheritance);
    tests = arrayAppend(tests, this.testInheritedMethod);
    tests = arrayAppend(tests, this.testThisMethod);
    tests = arrayAppend(tests, this.testSuperMethod);
    tests = arrayAppend(tests, this.testOverriddenMethodInChild);
    tests = arrayAppend(tests, this.testOverriddenMethodInParent);
    tests = arrayAppend(tests, this.testProperties);
    tests = arrayAppend(tests, this.testSetProperties);

    super.loadTests(tests);
  }
}