#import <Foundation/Foundation.h>

#import "BaseExample.h"
#import "Thing.h"
#import "Callback.h"

@interface Example : BaseExample

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

-(void) testPoke:(int) value;
-(void) testPeek:(int) value;
-(NSString *) getMessage;
-(NSString *) reverseIt:(NSString *) input;

@end
