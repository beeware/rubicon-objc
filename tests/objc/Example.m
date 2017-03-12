#import "Example.h"
#import <stdio.h>

@implementation Example

@synthesize intField = _intField;
@synthesize thing = _thing;
@synthesize callback = _callback;

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
    return self;
}

-(id) initWithIntValue: (int) v
{
    self = [super initWithIntValue:44];

    if (self) {
        [self setIntField:v];
    }
    return self;
}

-(id) initWithBaseIntValue: (int) b intValue: (int) v
{
    self = [super initWithIntValue:b];

    if (self) {
        [self setIntField:v];
    }
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

@end