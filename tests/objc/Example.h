#import <Foundation/Foundation.h>

#import "BaseExample.h"
#import "Thing.h"
#import "Callback.h"

struct simple {
	int foo;
	int bar;
};

struct complex {
	short things[4];
	void (*callback)(void);
	struct simple s;
	struct complex *next;
};

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

extern NSString *const SomeGlobalStringConstant;

@interface Example : BaseExample {

    int _intField;
    Thing *_thing;
    NSArray *_array;
    NSDictionary *_dict;
    id<Callback> _callback;
    int _ambiguous;
}

#if __has_extension(objc_class_property)
@property (class, readonly) int classAmbiguous;
#endif

@property int intField;
@property (retain) Thing *thing;
@property (retain) NSArray *array;
@property (retain) NSDictionary *dict;
@property (retain) id<Callback> callback;
@property (readonly) int ambiguous;

+(Protocol *)callbackProtocol;

+(int) staticIntField;
+(void) setStaticIntField: (int) v;

+(int) accessStaticIntField;
+(void) mutateStaticIntFieldWithValue: (int) v;

-(id) init;
-(id) initWithClassChange;
-(id) initWithIntValue: (int) v;
-(id) initWithBaseIntValue: (int) b intValue: (int) v;

-(int) accessIntField;
-(void) mutateIntFieldWithValue: (int) v;

-(void) setSpecialValue: (int) v;

-(void) mutateThing: (Thing *) thing;
-(Thing *) accessThing;

-(int) instanceMethod;
-(int) instanceAmbiguous;
+(int) classMethod;
+(int) classAmbiguous;

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
+(NSUInteger) overloaded:(NSUInteger)arg1 extraArg1:(NSUInteger)arg2 extraArg2:(NSUInteger)arg3;
+(NSUInteger) overloaded:(NSUInteger)arg1 extraArg2:(NSUInteger)arg2 extraArg1:(NSUInteger)arg3;
+(NSUInteger) overloaded:(NSUInteger)arg1 orderedArg1:(NSUInteger)arg2 orderedArg2:(NSUInteger)arg3;
+(NSUInteger) overloaded:(NSUInteger)arg1 duplicateArg:(NSUInteger)arg2 duplicateArg:(NSUInteger)arg3;

+(struct complex) doStuffWithStruct:(struct simple)simple;

-(id) processDictionary:(NSDictionary *) dict;
-(id) processArray:(NSArray *) dict;

-(NSSize) testThing:(int) value;

@end
