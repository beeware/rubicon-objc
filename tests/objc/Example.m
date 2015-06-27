#import "Example.h"
#import <stdio.h>

@implementation Example;

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
    return [[NSString alloc] initWithFormat:@"This is an ObjC Example object"];
}

-(NSString *) duplicateString:(NSString *) in
{
    return [[NSString alloc] initWithFormat:@"%@%@", in, in];
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

@end