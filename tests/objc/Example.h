#import <Foundation/Foundation.h>

#import "BaseExample.h"
#import "Thing.h"
#import "Callback.h"

/* objc_msgSend on i386, x86_64, ARM64; objc_msgSend_stret on ARM32. */
struct int_sized {
    char data[4];
};

/* objc_msgSend on x86_64, ARM64; objc_msgSend_stret on i386, ARM32. */
struct oddly_sized {
    char data[5];
};

/* objc_msgSend on ARM64; objc_msgSend_stret on i386, x86_64, ARM32. */
struct large {
    char data[17];
};

@interface Example : BaseExample {
    int _intField;
    Thing *_thing;
    id<Callback> _callback;
}

@property int intField;
@property (retain) Thing *thing;
@property (retain) id<Callback> callback;

+(int) staticIntField;
+(void) setStaticIntField: (int) v;

+(int) accessStaticIntField;
+(void) mutateStaticIntFieldWithValue: (int) v;

-(id) init;
-(id) initWithIntValue: (int) v;
-(id) initWithBaseIntValue: (int) b intValue: (int) v;

-(int) accessIntField;
-(void) mutateIntFieldWithValue: (int) v;

-(void) setSpecialValue: (int) v;

-(void) mutateThing: (Thing *) thing;
-(Thing *) accessThing;

-(NSString *) toString;
-(NSString *) duplicateString:(NSString *) in;
-(NSString *) smiley;

-(NSNumber *) theAnswer;
-(NSNumber *) twopi;

-(float) areaOfSquare: (float) size;
-(double) areaOfCircle: (double) diameter;
-(NSDecimalNumber *) areaOfTriangleWithWidth: (NSDecimalNumber *) width andHeight: (NSDecimalNumber *) height;

-(struct int_sized) intSizedStruct;
-(struct oddly_sized) oddlySizedStruct;
-(struct large) largeStruct;

-(void) testPoke:(int) value;
-(void) testPeek:(int) value;
-(NSString *) getMessage;
-(NSString *) reverseIt:(NSString *) input;

+(NSUInteger) overloaded;
+(NSUInteger) overloaded:(NSUInteger)arg1;
+(NSUInteger) overloaded:(NSUInteger)arg1 extraArg:(NSUInteger)arg2;

@end
