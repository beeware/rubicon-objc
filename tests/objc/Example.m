#import "Example.h"
#import "Altered_Example.h"
#import <stdio.h>
#import <objc/runtime.h>

NSString *const SomeGlobalStringConstant = @"Some global string constant";

@implementation Example

@synthesize intField = _intField;
@synthesize thing = _thing;
@synthesize array = _array;
@synthesize dict = _dict;
@synthesize callback = _callback;
@synthesize ambiguous = _ambiguous;

+(Protocol *)callbackProtocol {
    // Since the Callback protocol is not adopted by any class in the test harness, the compiler doesn't generate
    // runtime info for it by default. To force the protocol to be available at runtime, we use it as an object here.
    return @protocol(Callback);
}

static int _staticIntField = 11;

+(int) staticIntField
{
    @synchronized(self) {
        return _staticIntField;
    }
}

+(void) setStaticIntField: (int) v
{
    @synchronized(self) {
        _staticIntField = v;
    }
}

+(int) accessStaticIntField
{
    @synchronized(self) {
        return _staticIntField;
    }
}

+(void) mutateStaticIntFieldWithValue: (int) v
{
    @synchronized(self) {
        _staticIntField = v;
    }
}


-(id) init
{
    self = [super initWithIntValue:22];

    if (self) {
        [self setIntField:33];
    }
    _ambiguous = 42;
    return self;
}

-(id) initWithClassChange
{
    self = [super initWithIntValue:44];

    if (self) {
        [self setIntField:55];
    }
    _ambiguous = 37;

    object_setClass(self, [Altered_Example class]);
    return self;
}

-(id) initWithIntValue: (int) v
{
    self = [super initWithIntValue:44];

    if (self) {
        [self setIntField:v];
    }
    _ambiguous = 42;
    return self;
}

-(id) initWithBaseIntValue: (int) b intValue: (int) v
{
    self = [super initWithIntValue:b];

    if (self) {
        [self setIntField:v];
    }
    _ambiguous = 42;
    return self;
}

/* Simple methods */
-(int) accessIntField
{
    return self.intField;
}

-(void) mutateIntFieldWithValue: (int) v
{
    self.intField = v;
}

-(void) setSpecialValue: (int) v
{
    self.intField = v;
}

/* Float/Double/Decimal argument/return value handling */
-(float) areaOfSquare: (float) size
{
    return size * size;
}

-(double) areaOfCircle: (double) diameter
{
    return diameter * M_PI;
}

-(NSDecimalNumber *) areaOfTriangleWithWidth: (NSDecimalNumber *) width
                                   andHeight: (NSDecimalNumber *) height
{
    return [width decimalNumberByMultiplyingBy:[height decimalNumberByDividingBy:[NSDecimalNumber decimalNumberWithString:@"2.0"]]];
}

/* Handling of struct returns of different sizes. */
-(struct int_sized) intSizedStruct {
    struct int_sized ret = {"abc"};
    return ret;
}

-(struct oddly_sized) oddlySizedStruct {
    struct oddly_sized ret = {"abcd"};
    return ret;
}

-(struct large) largeStruct {
    struct large ret = {"abcdefghijklmnop"};
    return ret;
}


/* Handling of object references. */
-(void) mutateThing: (Thing *) thing
{
    self.thing = thing;
}

-(Thing *) accessThing
{
    return self.thing;
}

-(int) instanceMethod
{
    return _ambiguous;
}

-(int) instanceAmbiguous
{
    return _ambiguous;
}

+(int) classMethod
{
    return 37;
}

+(int) classAmbiguous
{
    return 37;
}

/* String argument/return value handling */
-(NSString *) toString
{
    return [NSString stringWithFormat:@"This is an ObjC Example object"];
}

-(NSString *) duplicateString:(NSString *) in
{
    return [NSString stringWithFormat:@"%@%@", in, in];
}

-(NSString *) smiley
{
    return @"%-)";
}

/* NSNumber return value */
-(NSNumber *) theAnswer
{
    return [NSNumber numberWithInt:42];
}

-(NSNumber *) twopi
{
    return [NSNumber numberWithFloat:2.0*M_PI];
}

/* Callback handling */
-(void) testPoke:(int) value
{
    [self.callback poke:self withValue:value];
}

-(void) testPeek:(int) value
{
    [self.callback peek:self withValue:value];
}

-(NSString *) getMessage
{
    return [self.callback message];
}

-(NSString *) reverseIt:(NSString *) input
{
    return [self.callback reverse:input];
}

+(NSUInteger) overloaded
{
    return 0;
}

+(NSUInteger) overloaded:(NSUInteger)arg1
{
    return arg1;
}

+(NSUInteger) overloaded:(NSUInteger)arg1 extraArg:(NSUInteger)arg2
{
    return arg1 + arg2;
}

+(NSUInteger) overloaded:(NSUInteger)arg1 extraArg1:(NSUInteger)arg2 extraArg2:(NSUInteger)arg3
{
    return arg1 + arg2 + arg3;
}

+(NSUInteger) overloaded:(NSUInteger)arg1 extraArg2:(NSUInteger)arg2 extraArg1:(NSUInteger)arg3
{
    return arg1 * arg2 * arg3;
}

+(NSUInteger) overloaded:(NSUInteger)arg1 orderedArg1:(NSUInteger)arg2 orderedArg2:(NSUInteger)arg3
{
    return 0;
}

+(NSUInteger) overloaded:(NSUInteger)arg1 duplicateArg:(NSUInteger)arg2 duplicateArg:(NSUInteger)arg3
{
    return arg1 + 2 * arg2 + 3 * arg3;
}

+(struct complex) doStuffWithStruct:(struct simple)simple
{
    return (struct complex){
        .things = {1, 2, 3, 4},
        .callback = NULL,
        .s = simple,
        .next = NULL,
    };
}

+(struct simple) extractSimpleStruct:(struct complex)complex
{
    return complex.s;
}

-(id) processDictionary:(NSDictionary *) dict
{
    return [dict objectForKey:@"data"];
}

-(id) processArray:(NSArray *) array
{
    return [array objectAtIndex:1];
}

-(NSSize) testThing:(int) value
{
    return [_thing computeSize:NSMakeSize(0, value)];
}

@end
