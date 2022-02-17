#import <Foundation/Foundation.h>

#import "Protocols.h"

@interface BaseExample : NSObject <ExampleProtocol, DerivedProtocol> {
    int _baseIntField;
}

@property int baseIntField;

+(int) staticBaseIntField;
+(void) setStaticBaseIntField: (int) v;

+(int) accessStaticBaseIntField;
+(void) mutateStaticBaseIntFieldWithValue: (int) v;

-(id) init;
-(id) initWithIntValue: (int) v;

-(int) accessBaseIntField;
-(void) mutateBaseIntFieldWithValue: (int) v;

-(void) method:(int) v withArg: (int) m;
-(void) methodWithArgs: (int) m, ...;
-(void) method:(int) v;

@end
